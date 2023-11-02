# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import contextlib
import logging
import os
import shlex
import shutil
import subprocess
import typing as tp
from pathlib import Path

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from .._util import subprocess_run
from ._00_extra_level import ExtraLevel
from ._03_meta import MetaMixin

__all__ = ["MultiManageMixin"]


class MultiManageMixin(MetaMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("projects",)

    def demodata(self) -> None:
        super().demodata()
        self.auxcon.multimanage = _ProtoNamespace(projects=["./admem"])

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "multimanage")
        for key in self.__keys():
            self._to_list("multimanage", key)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("multimanage", _ProtoNamespace())
        for key in self.__keys():
            self.auxd.multimanage.setdefault(key, [])

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.multimanage
        data.projects = list(map(Path, data.projects))
        for project in data.projects:
            if not project.exists():
                raise RuntimeError(f"project {project} does not exist")

    def mm_update(self, all_vip_branches: bool = False, prune: bool = False) -> None:
        for project in self.auxe.multimanage.projects:
            auxcon = self.get_subproject(project, level=ExtraLevel.RAW)
            with self.project_header(auxcon), self.preserve_cwd(project):
                branches = list(auxcon.gitlab["vip_branches"].keys())
                if not all_vip_branches:
                    branches = branches[:1]

                self.subprocess_run_shlex("git fetch --all")
                # reversed, as we want to end up on default
                for branch in reversed(branches):
                    self.subprocess_run_shlex(f"git checkout {branch}")
                    self.subprocess_run_shlex("git pull")
                if prune:
                    self.subprocess_run_shlex("git fetch -p")
                    lbranches = self.subprocess_run_shlex_out(
                        "git branch --format='%(refname:short)'"
                    ).split("\n")
                    rbranches = self.subprocess_run_shlex_out(
                        "git branch -r --format='%(refname:short)'"
                    ).split("\n")
                    for lbra in lbranches:
                        if not any(lbra in rbra for rbra in rbranches):
                            ans = self._prompt(  # type: ignore
                                f"delete local branch '{lbra}' (y/n)", fg="red"
                            )
                            if ans not in "yY":
                                continue
                            self.subprocess_run_shlex(f"git branch -D {lbra}")

    def get_subproject(
        self, project: Path, level: ExtraLevel = ExtraLevel.ENRICHED
    ) -> _ProtoNamespace:
        with self.preserve_cwd():
            # pylint: disable=too-many-function-args,unexpected-keyword-arg
            x = self.__class__(project, silent=True)  # type: ignore
            x.load_auxcon()
            with x.extra(level=level) as aux:  # type: ignore
                return aux  # type: ignore

    def mm_adaux(self, cmd_str: str) -> None:
        verbose = "-n"
        if logger.getEffectiveLevel() == logging.DEBUG:
            verbose = " -nv"
        self.mm_run(f"adaux {verbose} {cmd_str}")

    def mm_run(self, cmd_str: str) -> None:
        for project in self.auxe.multimanage.projects:
            auxcon = self.get_subproject(project, level=ExtraLevel.RAW)
            with self.project_header(auxcon), self.preserve_cwd(project):
                project_cmd_str = cmd_str
                self.subprocess_run_shlex(project_cmd_str, capture_output=False)

    @contextlib.contextmanager
    def project_header(self, auxcon: _ProtoNamespace) -> tp.Iterator[None]:
        columns, _ = shutil.get_terminal_size((80, 20))
        res = auxcon.project.name
        pad = columns - len(res) - 1
        self._print(res + " " + pad * ">", fg="white")
        yield
        # self._print(pad * "<" + " " + res, fg="yellow")

    @contextlib.contextmanager
    def preserve_cwd(self, new_path: tp.Optional[Path] = None) -> tp.Iterator[None]:
        original_cwd = Path.cwd()
        if new_path:
            logger.info("cwd changed to %s", new_path)
            os.chdir(new_path)
        yield
        logger.info("cwd changed to %s", original_cwd)
        os.chdir(original_cwd)

    def subprocess_run_shlex(
        self, cmd_str: str, *args: tp.Any, show: bool = True, **kwgs: tp.Any
    ) -> "subprocess.CompletedProcess[bytes]":
        kwgs.setdefault("check", True)
        kwgs.setdefault("capture_output", True)
        if show:
            columns, _ = shutil.get_terminal_size((80, 20))
            msg = f"> {cmd_str}"
            padding = columns - len(msg)
            self._print(msg, fg="blue", nl=not kwgs["capture_output"])
        cmd = shlex.split(cmd_str)
        try:
            res = subprocess_run(cmd, *args, **kwgs)
            if show and kwgs["capture_output"]:
                self._print((padding - 4) * " " + "[ok]", fg="blue")
            return res
        except subprocess.CalledProcessError as err:
            raise RuntimeError(f"error when running {cmd}, see error above") from err

    def subprocess_run_shlex_out(self, *args: tp.Any, **kwgs: tp.Any) -> str:
        kwgs.setdefault("show", False)
        kwgs.setdefault("capture_output", True)
        if not kwgs["capture_output"]:
            raise RuntimeError("cannot use output_as and capture_output=False")

        res = self.subprocess_run_shlex(*args, **kwgs)

        return res.stdout.decode().strip()
