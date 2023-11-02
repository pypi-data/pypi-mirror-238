#!/usr/bin/env python3
import importlib
import sys
import tomllib
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Self

from IPython.core.getipython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display_html

from .data import Data
from .handlers import magics, modules
from .misc import Misc
from .pandas import PandasTricks
from .util import import_formatter, is_ipy_support_html, merge_dicts

__helper_path__ = Path(__file__).parent
__cwd__ = Path.cwd()
__default_config__ = __helper_path__ / "default.toml"
__override_config__ = __cwd__ / "helper_config.toml"
__override_handlers__ = __cwd__ / "helper_handlers.py"


def func_lst_to_dict(lst: List) -> Dict:
    return {func.__name__: func for func in lst}


class Helper:
    """
    Helper class for setting up IPython.
    useage:
        `
        from helper import Helper
        helper = Helper(scope=globals())
        helper.set_global_values().import_libs().run_magics().done()
        `
        or just
        `
        helper.done()
        `
    """

    ipy: InteractiveShell
    config: Dict

    def __init__(
        self,
        scope: Dict,
        override_config: Optional[Path | str] = None,
        override_handlers: Optional[Path | str] = None,
        default_config: Optional[Path | str] = None,
        cwd: Optional[Path | str] = None,
    ) -> None:
        cwd = __cwd__ if cwd is None else Path(cwd)
        self.scope = scope
        self.default_config = (
            __default_config__ if default_config is None else Path(default_config)
        )
        self.override_config: Path = (
            __override_config__ if override_config is None else Path(override_config)
        )
        self.override_handlers = (
            __override_handlers__
            if override_handlers is None
            else Path(override_handlers)
        )
        self.is_global_values_ran = False
        self.is_import_libs_ran = False
        self.is_run_magics_ran = False
        self.fake_run: Dict[str, List] = dict(global_values=[], modules=[])
        ipy = get_ipython()
        if ipy is None:
            raise RuntimeError("IPython not found.")
        self.ipy = ipy
        self.is_ipy_support_html = is_ipy_support_html()
        self.modules = func_lst_to_dict(modules)
        self.magics = func_lst_to_dict(magics)
        self.config = self._read_config()
        self._register_modules()
        self._extend_handlers()

    def set_global_values(self) -> Self:
        global_values = self.config.get("globalvalues")
        if not global_values:
            return self
        for name, value in global_values.items():
            self.scope[name] = value
            print(f"{name} is set to {value}")
            # support simple numbers only
            self.fake_run["global_values"].append(f"{name} = {value}")
        return self

    def import_libs(self) -> Self:
        module_specs = self.config["modules"]
        for name, spec in module_specs.items():
            func = self.modules.get(name)
            if callable(func):
                success = func(helper=self, spec=spec)
                if success and spec.get("insert"):
                    self.fake_run["modules"].append(import_formatter(spec))
        return self

    def run_magics(self) -> Self:
        magic_specs = self.config["magics"]
        for name, spec in magic_specs.items():
            func = self.magics.get("magic_" + name)
            if callable(func):
                func(helper=self, spec=spec)
        return self

    def done(self) -> Self:
        if not self.is_global_values_ran:
            self.set_global_values()
        if not self.is_import_libs_ran:
            self.import_libs()
        if not self.is_run_magics_ran:
            self.run_magics()
        done_mes = "👏Helper initiallized." + " You may need to del some import lines."
        if self.is_ipy_support_html:
            display_html(done_mes)
            display_html("<b>Import and Settings</b>", raw=True)
            insert_lines = (
                "\n".join(self.fake_run["modules"])
                + "\n"
                + "\n".join(self.fake_run["global_values"])
            )
            self.ipy.set_next_input(insert_lines)
        else:
            print(done_mes)
        return self

    def _extend_handlers(self):
        if not self.override_handlers.name.endswith(".py"):
            warnings.warn("override_handlers is not a python file.")
            return
        sys.path.append(str(self.override_handlers.absolute().parent))
        override_handlers_package = self.override_handlers.stem
        try:
            override_handlers = importlib.import_module(name=override_handlers_package)
            if hasattr(override_handlers, "modules"):
                modules = override_handlers.modules
                self.modules.update(func_lst_to_dict(modules))
            if hasattr(override_handlers, "magics"):
                magics = override_handlers.magics
                self.magics.update(func_lst_to_dict(magics))
        except ModuleNotFoundError:
            return

    def _read_config(self) -> Dict:
        config: Dict
        config_path = __default_config__
        with open(config_path, mode="rb") as file:
            config = tomllib.load(file)
        current_config_path = __override_config__
        if current_config_path.exists():
            with open(current_config_path, mode="rb") as file:
                current_config = tomllib.load(file)
                config = merge_dicts(config, current_config)
        return config

    def _register_modules(self):
        self.data = Data()
        self.misc = Misc(ipy=self.ipy, support_html=self.is_ipy_support_html)
        self.pandas = PandasTricks(support_html=self.is_ipy_support_html)
