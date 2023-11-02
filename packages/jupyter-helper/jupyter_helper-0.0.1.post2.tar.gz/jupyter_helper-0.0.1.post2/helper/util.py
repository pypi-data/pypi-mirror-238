import functools
import importlib
import importlib.util
import warnings
from types import ModuleType
from typing import Any, Callable, Dict

from IPython.display import display


def handler_get_lib(scope: Dict, spec: Dict) -> ModuleType:
    _as = spec.get("as")
    if _as is None:
        raise ModuleNotFoundError(f"{_as} is not imported.")
    return scope[_as]


def magic_handler(func: Callable) -> Any:
    @functools.wraps(func)
    def inner(self, *args, **kwargs) -> Any:
        if self.ipy is None:
            raise RuntimeError("IPython not found.")
        return func(self, *args, **kwargs)

    return inner


def module_handler(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(**kwargs) -> bool:
        spec = kwargs.get("spec")
        helper = kwargs.get("helper")
        if helper is None:
            return False
        if spec is None:
            return False
        if not spec.get("enabled"):
            return False
        _from = spec.get("from")
        _import = spec.get("import")
        assert _import is not None
        _attr = spec.get("attr", False)
        _as = spec["as"]
        if _as is False:
            _as = _import
        if _from is not None:
            # need import from first then as
            if importlib.util.find_spec(_from) is None:
                print("Module not found:", _from)
                return False
            if not _attr:
                lib = importlib.import_module(
                    name="." + _import,
                    package=_from,
                )
            else:
                lib_parent = importlib.import_module(name=_from)
                lib = getattr(lib_parent, _import)
        else:
            if importlib.util.find_spec(_import) is None:
                print("Module not found:", _import)
                return False
            lib = importlib.import_module(name=_import)
        # override imported module
        helper.scope[_as] = lib
        result: bool = func(helper, spec)
        return result

    return inner


def merge_dicts(default: Dict, current: Dict):
    for key, value in current.items():
        if (
            isinstance(value, dict)
            and key in default
            and isinstance(default[key], dict)
        ):
            default[key] = merge_dicts(default[key], value)
        else:
            default[key] = value
    return default


def import_formatter(spec: Dict) -> str:
    _from = spec.get("from")
    _import = spec.get("import")
    _attr = spec.get("attr", False)
    _as = spec.get("as")
    if _as is False:
        _as = _import
    ret = ""
    if _from is not None:
        if not _attr:
            ret = f"from {_from} import {_import} as {_as}"
        else:
            ret = f"import {_from}\n" + f"{_as} = {_from}.{_import}"
    else:
        ret = f"import {_import} as {_as}"

    return ret


def is_ipy_support_html() -> bool:
    class DisplayInspector:
        """Objects that display as HTML or plain."""

        def __init__(self) -> None:
            self.on = "Plain"

        def _repr_html_(self) -> str:
            self.on = "HTML"
            return ""

        def __repr__(self) -> str:
            self.on = "Plain"
            return ""

    inspector = DisplayInspector()
    display(inspector)
    return inspector.on == "HTML"


def warn_html(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(self, *args, **kwargs) -> Any:
        class_name = self.__class__.__name__
        func_name = func.__name__
        if not self.support_html:
            warnings.warn(f"{class_name}.{func_name} HTML not supported")
            return
        return func(self, *args, **kwargs)

    return inner
