# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
from .._proto_namespace import _ProtoNamespace
from ._05_python_project import PythonProjectMixin


class EntryPointMixin(PythonProjectMixin):
    def formatted(self) -> None:
        super().formatted()
        if "entry_points" in self.auxcon:
            self.auxf.entry_points = _ProtoNamespace(self.auxcon.entry_points or {})

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("entry_points", _ProtoNamespace())

    def demodata(self) -> None:
        super().demodata()
        self.auxcon.entry_points = _ProtoNamespace()
        data = self.auxcon.entry_points
        data.plugin_hook = dict(plugin_name="plugin:func")

    def bake(self) -> None:
        super().bake()
        config = self.auxe.python_project.config
        data = self.auxe.entry_points
        config["options.entry_points"].update(data)
