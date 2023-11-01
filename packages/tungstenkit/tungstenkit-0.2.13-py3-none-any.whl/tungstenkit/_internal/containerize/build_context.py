import os
import shutil
import subprocess
import tempfile
import time
import typing as t
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from uuid import uuid4

import attrs
from filelock import FileLock
from pathspec import PathSpec
from rich.progress import Progress, TextColumn

from tungstenkit import exceptions
from tungstenkit._internal import storables
from tungstenkit._internal.configs import BuildConfig
from tungstenkit._internal.constants import TUNGSTEN_DIR_IN_CONTAINER
from tungstenkit._internal.logging import log_debug, log_info, log_warning
from tungstenkit._internal.utils.context import hide_traceback
from tungstenkit._internal.utils.docker_builder import create_files_image_tarball
from tungstenkit._internal.utils.docker_client import (
    load_docker_image_from_file,
    remove_docker_image,
)
from tungstenkit._internal.utils.file import (
    format_file_size,
    get_tree_size_in_bytes,
    is_relative_to,
)

from .dockerfiles import BaseDockerfile

TMP_DIR_NAME = ".tungsten-build"
LARGE_FILE_THRESHOLD = 100 * 1024**2  # 100MB


@attrs.define
class BuildContext:
    config: BuildConfig
    root_dir: Path
    dockerfile_path: Path

    def walk_fs(self) -> t.Generator[storables.SourceFile, None, None]:
        """
        Recursively yield files under ``TUNGSTEN_DIR_IN_CONTAINER`` in container fs
        """
        abs_root_dir = self.root_dir.resolve()
        include_spec = PathSpec.from_lines("gitwildmatch", self.config.include_files)
        exclude_spec = PathSpec.from_lines(
            "gitwildmatch", self.config.exclude_files + [TMP_DIR_NAME + "*/"]
        )

        for rel_path_str in include_spec.match_tree(self.root_dir, follow_links=False):
            posix_rel_path_str = Path(rel_path_str).as_posix()
            if not exclude_spec.match_file(posix_rel_path_str):
                abs_path_in_host_fs = abs_root_dir / rel_path_str
                size = (
                    abs_path_in_host_fs.lstat().st_size
                    if abs_path_in_host_fs.is_symlink()
                    else abs_path_in_host_fs.stat().st_size
                )
                yield storables.SourceFile(
                    abs_path_in_host_fs=abs_path_in_host_fs,
                    rel_path_in_model_fs=PurePosixPath(posix_rel_path_str),
                    size=size,
                )
        if self.config.copy_files:
            for pathstr_in_host_fs, pathstr_in_model_fs in self.config.copy_files:
                abs_path_in_host_fs = Path(pathstr_in_host_fs)
                if not abs_path_in_host_fs.is_absolute():
                    abs_path_in_host_fs = abs_root_dir / abs_path_in_host_fs

                path_in_model_fs = PurePosixPath(pathstr_in_model_fs)
                if path_in_model_fs.is_absolute():
                    if not is_relative_to(path_in_model_fs, TUNGSTEN_DIR_IN_CONTAINER):
                        continue
                    rel_path_in_model_fs = path_in_model_fs.relative_to(TUNGSTEN_DIR_IN_CONTAINER)
                else:
                    rel_path_in_model_fs = path_in_model_fs

                size = (
                    abs_path_in_host_fs.lstat().st_size
                    if abs_path_in_host_fs.is_symlink()
                    else abs_path_in_host_fs.stat().st_size
                )
                yield storables.SourceFile(
                    abs_path_in_host_fs=abs_path_in_host_fs,
                    rel_path_in_model_fs=rel_path_in_model_fs,
                    size=size,
                )

    def build(self, tag: str) -> None:
        subprocess_args = [
            "docker",
            "buildx",
            "build",
            f"--tag={tag}",
            "--cache-to=type=inline",
            "--file=" + str(self.dockerfile_path.relative_to(self.root_dir)),
            "--output=type=docker,compression=zstd,force-compression=true,push=false",
        ]
        subprocess_args.append(str(self.root_dir))
        log_debug(msg="$ " + " ".join(subprocess_args), pretty=False)
        res = subprocess.run(subprocess_args, check=False, env={"DOCKER_BUILDKIT": "1"})

        if res.returncode != 0:
            with hide_traceback():
                raise exceptions.BuildError(
                    f"Failed to build {tag}. For the reason, refer to above build logs."
                )


@contextmanager
def setup_build_ctx(
    build_config: BuildConfig,
    build_dir: Path,
    module_path: Path,
    dockerfile_generator: BaseDockerfile,
):
    assert build_dir.is_absolute()
    assert module_path.is_absolute()
    try:
        rel_path_to_module = module_path.relative_to(build_dir)
    except ValueError:
        raise exceptions.BuildError(
            f"Python module '{module_path}' is outside build dir at '{build_dir}'"
        )

    log_info(
        f"Add files from '{build_dir.resolve()}' to container"
        f"\n include_files: {build_config.include_files}"
        f"\n exclude_files: {build_config.exclude_files}\n"
    )
    build_config.include_files.append(("/" / rel_path_to_module).as_posix())

    # Prepare tmp dir
    rel_path_to_tmp_dir = Path(TMP_DIR_NAME)
    try:
        lock_path = rel_path_to_tmp_dir / ".tungsten-build.lock"
        if lock_path.exists() and FileLock(lock_path).is_locked:
            raise exceptions.BuildError(
                "A build is already in progress. Restart after the build in progress is complete."
            )
        if rel_path_to_tmp_dir.exists():
            shutil.rmtree(rel_path_to_tmp_dir)

        rel_path_to_tmp_dir.mkdir()

        with FileLock(lock_path):
            with ThreadPoolExecutor(max_workers=8) as executor:
                with _large_files_image(
                    build_dir, build_config.include_files, build_config.exclude_files
                ) as (
                    large_file_rel_paths,
                    large_files_image_name,
                ):
                    # TODO handle the case where copy_files include large files

                    rel_path_to_dockerfile = rel_path_to_tmp_dir / "Dockerfile"
                    future_list: t.List[Future] = []

                    build_config.copy_files.extend(
                        _convert_abs_symlinks_to_rel(
                            build_dir,
                            include_patterns=build_config.include_files,
                            exclude_patterns=build_config.exclude_files,
                            rel_path_to_tmp_dir=rel_path_to_tmp_dir,
                        )
                    )
                    if build_config.copy_files:
                        build_config.copy_files = _copy_files(
                            abs_path_to_build_dir=build_dir,
                            rel_path_to_tmp_dir=rel_path_to_tmp_dir,
                            include_with_dest=build_config.copy_files,
                            executor=executor,
                            future_list=future_list,
                        )
                        _show_progress_while_copying_files(
                            copy_dir=rel_path_to_tmp_dir,
                            future_list=future_list,
                            ignore_patterns=["tungstenkit"],
                        )

                    dockerfile = dockerfile_generator.generate(
                        tmp_dir_in_build_ctx=rel_path_to_tmp_dir,
                        large_files_image_name=large_files_image_name,
                        large_file_rel_paths=large_file_rel_paths,
                    )
                    dockerfile_path = build_dir / rel_path_to_dockerfile
                    dockerfile_path.write_text(dockerfile)
                    log_debug(
                        "Dockerfile:\n"
                        + "\n".join(
                            ["  " + line for line in dockerfile.strip().split("\n") if line]
                        ),
                        pretty=False,
                    )

                    dockerignore_lines = _get_dockerignore_lines(
                        build_dir,
                        build_config.include_files,
                        build_config.exclude_files,
                    )
                    log_debug("")
                    log_debug(
                        ".dockerignore:\n"
                        + "\n".join([" " + line for line in dockerignore_lines]),
                        pretty=False,
                    )
                    dockerignore_path = Path(str(dockerfile_path) + ".dockerignore")
                    with dockerignore_path.open("w") as f:
                        for line in dockerignore_lines:
                            f.write(line + "\n")
                    log_debug(f"Saved .dockerignore at {dockerignore_path}")
                    log_debug("")

                    yield BuildContext(
                        config=build_config,
                        root_dir=build_dir,
                        dockerfile_path=dockerfile_path,
                    )
    finally:
        shutil.rmtree(rel_path_to_tmp_dir)


def _convert_abs_symlinks_to_rel(
    abs_path_to_build_dir: Path,
    include_patterns: t.List[str],
    exclude_patterns: t.List[str],
    rel_path_to_tmp_dir: Path,
) -> t.List[t.Tuple[str, str]]:
    link_and_target_pairs: t.List[t.Tuple[str, str]] = []
    include_spec = PathSpec.from_lines("gitwildmatch", include_patterns)
    exclude_spec = PathSpec.from_lines(
        "gitwildmatch", exclude_patterns + [rel_path_to_tmp_dir.as_posix()]
    )
    for link_path in list(abs_path_to_build_dir.rglob("*")):
        if not link_path.is_symlink():
            continue

        pattern = link_path.relative_to(abs_path_to_build_dir).as_posix()
        if include_spec.match_file(pattern) and not exclude_spec.match_file(pattern):
            orig_target = Path(os.readlink(str(link_path)))

            if not orig_target.is_absolute():
                continue

            if not orig_target.exists():
                log_warning(f"Target of symbolic link '{link_path}' does not exist")
                continue

            try:
                orig_target.relative_to(abs_path_to_build_dir)
            except ValueError:
                raise exceptions.BuildError(
                    f"Target '{orig_target}' of link '{link_path}' is outside build dir at "
                    f"'{abs_path_to_build_dir}'"
                )
            tmp_link_path = (
                abs_path_to_build_dir
                / rel_path_to_tmp_dir
                / "symlinks"
                / link_path.relative_to(abs_path_to_build_dir)
            )
            new_target = os.path.relpath(orig_target, start=tmp_link_path)
            tmp_link_path.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(new_target, tmp_link_path)
            log_debug(f"Change target of link '{link_path}': '{orig_target}' -> '{new_target}'")
            link_and_target_pairs.append(
                (
                    str(tmp_link_path),
                    link_path.relative_to(abs_path_to_build_dir).as_posix(),
                )
            )

    return link_and_target_pairs


def _copy_files(
    abs_path_to_build_dir: Path,
    rel_path_to_tmp_dir: Path,
    include_with_dest: t.List[t.Tuple[str, str]],
    executor: ThreadPoolExecutor,
    future_list: t.List[Future],
) -> t.List[t.Tuple[str, str]]:
    if len(include_with_dest) > 0:
        log_info("Copy extra files to container")

    files_with_dest: t.List[t.Tuple[str, str]] = []
    for src_str, dest_str in include_with_dest:
        src_in_host = Path(src_str)
        src_in_host = (
            src_in_host if src_in_host.is_absolute() else abs_path_to_build_dir / src_in_host
        )
        if not src_in_host.is_symlink() and not src_in_host.exists():
            raise exceptions.BuildError(
                f"Failed to copy '{src_str}' to '{dest_str}'. '{src_str}' does not exist."
            )
        tmp_dir = abs_path_to_build_dir / rel_path_to_tmp_dir
        if is_relative_to(src_in_host, tmp_dir):
            src_in_build_ctx = src_in_host
        else:
            log_info(f" '{src_str}' (host) -> '{dest_str}' (container)")
            src_in_build_ctx = (
                abs_path_to_build_dir / rel_path_to_tmp_dir / uuid4().hex / src_in_host.name
            )
            if src_in_host.is_symlink() or src_in_host.is_file():
                future_list.append(
                    executor.submit(
                        shutil.copy, str(src_in_host), str(src_in_build_ctx), follow_symlinks=False
                    )
                )
            else:
                src_in_build_ctx.mkdir(exist_ok=True, parents=True)
                for element in src_in_host.iterdir():
                    if element.is_dir():
                        future_list.append(
                            executor.submit(
                                shutil.copytree,
                                str(element),
                                str(src_in_build_ctx / element.name),
                                symlinks=False,
                                ignore_dangling_symlinks=True,
                            )
                        )
                    else:
                        future_list.append(
                            executor.submit(
                                shutil.copy,
                                str(element),
                                str(src_in_build_ctx / Path(element).name),
                            )
                        )
        files_with_dest.append(
            (src_in_build_ctx.relative_to(abs_path_to_build_dir).as_posix(), dest_str)
        )

    log_info("")
    return files_with_dest


def _show_progress_while_copying_files(
    copy_dir: Path, future_list: t.List[Future], ignore_patterns: t.Optional[t.List[str]] = None
):
    progress = Progress(TextColumn("{task.description}"))
    desc_prefix = "Copied: "
    task = progress.add_task(desc_prefix + "0B")
    with progress:
        while not all(fut.done() for fut in future_list):
            size_in_bytes = get_tree_size_in_bytes(
                root_dir=copy_dir, ignore_patterns=ignore_patterns
            )
            human_readable_size = format_file_size(size_in_bytes)
            progress.update(task, description=desc_prefix + human_readable_size)
            time.sleep(0.1)

        size_in_bytes = get_tree_size_in_bytes(root_dir=copy_dir, ignore_patterns=["tungstenkit"])
        human_readable_size = format_file_size(size_in_bytes)
        progress.update(task, description=desc_prefix + human_readable_size)

    log_info("")


def _get_large_file_rel_paths(
    abs_path_to_build_dir: Path, include_files: t.List[str], exclude_files: t.List[str]
):
    include_spec = PathSpec.from_lines("gitwildmatch", include_files)
    exclude_spec = PathSpec.from_lines("gitwildmatch", exclude_files + [TMP_DIR_NAME + "*/"])
    candidates = list(
        p.relative_to(abs_path_to_build_dir)
        for p in abs_path_to_build_dir.rglob("*")
        if p.stat().st_size > LARGE_FILE_THRESHOLD and not p.is_symlink()
    )
    return list(
        p for p in candidates if include_spec.match_file(p) and not exclude_spec.match_file(p)
    )


def _get_dockerignore_lines(
    abs_path_to_build_dir: Path,
    include_files: t.List[str],
    exclude_files: t.List[str],
) -> t.List[str]:
    if len(include_files) == 0:
        return [""]

    dockerignore_lines = [
        p.as_posix()
        for p in _get_large_file_rel_paths(abs_path_to_build_dir, include_files, exclude_files)
    ]
    # dockerignore_lines = []

    include_spec = PathSpec.from_lines("gitwildmatch", include_files)
    exclude_spec = PathSpec.from_lines("gitwildmatch", exclude_files)

    def add(abs_path_to_root_dir: Path):
        for abs_path in abs_path_to_root_dir.glob("*"):
            rel_path = abs_path.relative_to(abs_path_to_build_dir)

            if rel_path.parts[0] == TMP_DIR_NAME:
                continue

            rel_path_posix_str = rel_path.as_posix()

            if abs_path.is_dir():
                if not (
                    (
                        include_spec.match_file(rel_path_posix_str)
                        and not exclude_spec.match_file(rel_path_posix_str)
                    )
                    or any(
                        PathSpec.from_lines("gitwildmatch", [rel_path_posix_str]).match_file(
                            pattern
                        )
                        for pattern in include_files
                    )
                ):
                    dockerignore_lines.append(rel_path_posix_str)
                else:
                    add(abs_path)
            else:
                if not include_spec.match_file(rel_path_posix_str) or exclude_spec.match_file(
                    rel_path_posix_str
                ):
                    dockerignore_lines.append(rel_path_posix_str)

    add(abs_path_to_build_dir)

    return dockerignore_lines


@contextmanager
def _large_files_image(
    abs_path_to_build_dir: Path, include_files: t.List[str], exclude_files: t.List[str]
):
    large_file_rel_paths = _get_large_file_rel_paths(
        abs_path_to_build_dir, include_files, exclude_files
    )
    if len(large_file_rel_paths) > 0:
        log_info("Create image with large files:")
        for large_file_rel_path in large_file_rel_paths:
            log_info(f" - {large_file_rel_path}")

        with tempfile.TemporaryDirectory(prefix="tungsten-build-") as tmpdir_str:
            large_files_image_name = "tungsten-lf-" + uuid4().hex[:7] + ":" + uuid4().hex[:7]
            large_files_image_tar_path = Path(tmpdir_str) / "large-files-image.tar"
            log_info("")
            create_files_image_tarball(
                large_files_image_name,
                [abs_path_to_build_dir / p for p in large_file_rel_paths],
                large_files_image_tar_path,
                abs_path_to_build_dir,
            )

            log_info("")

            log_info("Importing the image to docker")
            load_docker_image_from_file(large_files_image_tar_path)
            log_info("")
            try:
                yield (large_file_rel_paths, large_files_image_name)
            finally:
                remove_docker_image(large_files_image_name)
    else:
        yield ([], None)
