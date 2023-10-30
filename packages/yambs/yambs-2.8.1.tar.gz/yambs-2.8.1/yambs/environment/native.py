"""
A module implementing a native-build environment.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import Any, Dict, Optional, Set, TextIO

# third-party
from vcorelib.io import ARBITER
from vcorelib.logging import LoggerMixin
from vcorelib.paths import Pathlike, normalize

# internal
from yambs.aggregation import collect_files, populate_sources, sources_headers
from yambs.config.native import Native
from yambs.dependency.manager import DependencyManager
from yambs.generate.common import APP_ROOT, get_jinja, render_template
from yambs.generate.ninja import write_continuation
from yambs.generate.ninja.format import render_format
from yambs.generate.variants import generate as generate_variants
from yambs.translation import BUILD_DIR_PATH, get_translator


def resolve_build_dir(build_root: Path, variant: str, path: Path) -> Path:
    """Resolve the build-directory variable in a path."""
    return build_root.joinpath(variant, path.relative_to(BUILD_DIR_PATH))


def combine_if_not_absolute(root: Path, candidate: Pathlike) -> Path:
    """https://github.com/vkottler/ifgen/blob/master/ifgen/paths.py"""

    candidate = normalize(candidate)
    return candidate if candidate.is_absolute() else root.joinpath(candidate)


class NativeBuildEnvironment(LoggerMixin):
    """A class implementing a native-build environment."""

    def __init__(self, config: Native) -> None:
        """Initialize this instance."""

        super().__init__()

        self.config = config

        self.dependency_manager = DependencyManager(
            self.config.third_party_root, self.config.root
        )

        # Collect sources.
        self.sources = collect_files(config.src_root)
        self.apps: Set[Path] = set()
        self.regular: Set[Path] = set()
        self.third_party: Set[Path] = set()

        self.jinja = get_jinja()

    def render(self, root: Path, name: str) -> None:
        """Render a template."""

        with self.log_time("Render '%s'", root.joinpath(name)):
            render_template(
                self.jinja, root, f"native_{name}", self.config.data, out=name
            )

    def write_compile_line(self, stream: TextIO, path: Path) -> Path:
        """Write a single source-compile line."""

        translator = get_translator(path)
        from_src = path.relative_to(self.config.src_root)

        out = translator.output(from_src)

        stream.write(f"build {out}: {translator.rule} $src_dir/{from_src}")
        stream.write(linesep)

        return out

    def write_third_party_line(
        self, stream: TextIO, path: Path
    ) -> Optional[Path]:
        """Write a single source-compile line for a third-party source."""

        out = None

        try:
            # Get the relative part of the path from the third-party root.
            rel_part = path.relative_to(self.config.third_party_root)
        except ValueError:
            rel_part = Path("..", path.relative_to(self.config.root))

        # Ignore applications.
        if APP_ROOT not in str(rel_part):
            translator = get_translator(path)
            out = translator.translate(
                Path("$build_dir", "third-party", rel_part)
            )

            stream.write(
                f"build {out}: {translator.rule} $third_party_dir/{rel_part}"
            )
            stream.write(linesep)

        return out

    def write_source_rules(self, stream: TextIO) -> Set[Path]:
        """Write source rules."""

        result = {
            self.write_compile_line(stream, path) for path in self.regular
        }

        # Add third-party sources.
        for path in self.third_party:
            path_result = self.write_third_party_line(stream, path)
            if path_result is not None:
                result.add(path_result)

        return result

    def write_static_library_rule(
        self, stream: TextIO, outputs: Set[Path]
    ) -> Path:
        """Create a rule for a static library output."""

        lib = BUILD_DIR_PATH.joinpath(f"{self.config.project}.a")
        line = f"build {lib}: ar "
        offset = " " * len(line)

        list_outputs = list(outputs)
        stream.write(line + str(list_outputs[0]))
        for file in list_outputs[1:]:
            write_continuation(stream, offset)
            stream.write(str(file))

        stream.write(linesep + linesep)

        return lib

    def _write_app_phony_targets(
        self, stream: TextIO, elfs: Dict[Path, Path], uf2_family: str = None
    ) -> None:
        """Write phony targets for all variants."""

        elfs_list = list(elfs.values())

        if elfs_list:
            line = "build ${variant}_apps: phony "
            offset = " " * len(line)

            stream.write(line + str(elfs_list[0]))
            for elf in elfs_list[1:]:
                write_continuation(stream, offset)
                stream.write(str(elf))
            stream.write(linesep)

            if uf2_family:
                # Create uf2 phony.
                line = "build ${variant}_uf2s: phony "
                offset = " " * len(line)

                uf2s = [x.with_suffix(".uf2") for x in elfs_list]

                stream.write(line + str(uf2s[0]))
                for elf in uf2s[1:]:
                    write_continuation(stream, offset)
                    stream.write(str(elf))
                stream.write(linesep)

    def write_app_rules(
        self, stream: TextIO, outputs: Set[Path], uf2_family: str = None
    ) -> Dict[Path, Path]:
        """Write app rules."""

        elfs: Dict[Path, Path] = {}

        # Create rules for linked executables.
        for path in self.apps:
            out = self.write_compile_line(stream, path)

            from_src = path.relative_to(self.config.src_root)
            elf = BUILD_DIR_PATH.joinpath(from_src.with_suffix(".elf"))
            elfs[path] = elf
            line = f"build {elf}: link "
            offset = " " * len(line)

            stream.write(line + str(out))

            for file in outputs:
                write_continuation(stream, offset)
                stream.write(str(file))

            # Executables can't be linked until third-party dependencies are
            # actually built.
            stream.write(" | ${variant}_third_party")

            stream.write(linesep + linesep)

            # Write rules for other kinds of outputs.
            for output in ["bin", "hex", "dump"]:
                stream.write(
                    f"build {elf.with_suffix('.' + output)}: {output} {elf}"
                )
                stream.write(linesep)

            if uf2_family:
                stream.write(
                    (
                        f"build {elf.with_suffix('.uf2')}: "
                        f"uf2 {elf.with_suffix('.hex')}"
                    )
                )
                stream.write(linesep)

            stream.write(linesep)

        # Add a phony target for creating a static library.
        if outputs:
            stream.write(
                "build ${variant}_lib: phony "
                + str(self.write_static_library_rule(stream, outputs))
                + linesep
                + linesep
            )

        self._write_app_phony_targets(stream, elfs, uf2_family=uf2_family)

        return elfs

    def _render_app_manifest(self, elfs: Dict[Path, Path]) -> None:
        """Render the application manifest."""

        path = self.config.ninja_root.joinpath("apps.json")
        with self.log_time("Write '%s'", path):
            data: Dict[str, Any] = {}

            for app in self.apps:
                name = app.with_suffix("").name
                assert (
                    name not in data
                ), f"Duplicate app name '{name}' ({app})!"

                data[name] = {
                    "source": str(app),
                    "variants": {
                        variant: str(
                            resolve_build_dir(
                                self.config.build_root, variant, elfs[app]
                            )
                        )
                        for variant in self.config.data["variants"]
                    },
                }

            ARBITER.encode(
                path,
                {
                    "all": data,
                    "tests": [x for x in data if x.startswith("test_")],
                },
            )

    def _handle_extra_source_dirs(self) -> None:
        """Handle additional source directories (belonging to dependencies)."""

        # Recurse directories from the dependency manager.
        paths_recurse = [
            (path, True) for path in self.dependency_manager.source_dirs
        ]

        # Don't recurse directories provided by the configuration.
        paths_recurse.extend(
            [
                (combine_if_not_absolute(self.config.root, path), False)
                for path in self.config.data.get("extra_sources", [])
            ]
        )

        for path, recurse in paths_recurse:
            collect_files(path, files=self.sources, recurse=recurse)

    def generate(self, sources_only: bool = False) -> None:
        """Generate ninja files."""

        if not sources_only:
            # Audit dependencies.
            for dep in self.config.dependencies:
                self.dependency_manager.audit(dep)

            # Create build script.
            self.dependency_manager.save(
                self.config.third_party_script, logger=self.logger
            )

            # Handle compile and link flags generated by the third-party pass.
            self.config.data["common_cflags"].extend(
                self.dependency_manager.compile_flags
            )
            self.config.data["common_ldflags"].extend(
                self.dependency_manager.link_flags
            )

            self._handle_extra_source_dirs()
            populate_sources(
                self.sources,
                self.config.src_root,
                self.apps,
                self.regular,
                self.third_party,
            )

            # Render templates.
            generate_variants(
                self.jinja,
                self.config,
                self.config.data["cflag_groups"],
                self.config.data["ldflag_groups"],
            )
            self.render(self.config.root, "build.ninja")
            for template in ["all", "rules"]:
                self.render(self.config.ninja_root, f"{template}.ninja")

        # Render sources file.
        path = self.config.ninja_root.joinpath("sources.ninja")
        with self.log_time("Write '%s'", path):
            with path.open("w") as path_fd:
                outputs = self.write_source_rules(path_fd)

        # Render apps file.
        path = self.config.ninja_root.joinpath("apps.ninja")
        with self.log_time("Write '%s'", path):
            with path.open("w") as path_fd:
                elfs = self.write_app_rules(
                    path_fd, outputs, self.config.data.get("uf2_family")
                )

        # Render format file.
        render_format(
            self.config,
            {
                x
                for x in sources_headers(self.sources)
                if self.config.src_root in x.parents
            },
            root=self.config.root,
            suffix=self.config.data["variants"]["clang"]["suffix"],
        )

        # Render application manifest.
        self._render_app_manifest(elfs)
