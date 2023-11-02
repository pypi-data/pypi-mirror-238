from typing import Dict

from IPython.core.magic import MagicsManager

from .util import handler_get_lib, magic_handler, module_handler

__all__ = ["modules", "magics"]


@module_handler
def pyplot(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    # lib spec applies
    font_family = spec.get("font_family", "font.sans-serif")
    lib.rcParams[font_family] = [spec.get("font", "Noto Sans CJK JP")]
    lib.rcParams["axes.unicode_minus"] = spec.get(
        "fix_unicode_minus",
        True,
    )
    lib.rc("figure", dpi=spec.get("dpi", 300))
    print(f"matplotlib.pyplot: {lib.matplotlib.__version__}")
    return True


@module_handler
def scienceplots(helper, spec: Dict) -> bool:
    # handler_get_lib(helper.scope, spec)
    if "plt" not in helper.scope:
        return False
    helper.scope["plt"].style.use(
        spec.get("style", ["science", "no-latex", "cjk-jp-font"])
    )
    return True


@module_handler
def copydf(helper, spec: Dict) -> bool:
    handler_get_lib(helper.scope, spec)
    return True


@module_handler
def seaborn(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    context = spec.get("context", "notebook")
    style = spec.get("style", "ticks")
    font = spec.get("font", "Noto Sans CJK JP")
    font_scale = spec.get("font_scale", 1.2)
    lib.set(context=context, style=style, font=font, font_scale=font_scale)
    print(f"seaborn: {lib.__version__}")
    return True


@module_handler
def numpy(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    if spec.get("set_random_state"):
        lib.random.seed(
            seed=helper.config["globalvalues"].get("random_state", 42)
        )
    print(f"numpy: {lib.__version__}")
    return True


@module_handler
def numexpr(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    print(f"numexpr: {lib.__version__}")
    return True


@module_handler
def numba(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    print(f"numba: {lib.__version__}")
    return True


@module_handler
def sympy(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    print(f"sympy: {lib.__version__}")
    return True


@module_handler
def scipy(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    print(f"scipy: {lib.__version__}")
    return True


@module_handler
def pandas(helper, spec: Dict) -> bool:
    lib = handler_get_lib(helper.scope, spec)
    print(f"pandas: {lib.__version__}")
    return True


@magic_handler
def magic_matplotlib(helper, spec: Dict) -> bool:
    magic = helper.ipy.run_line_magic
    if not spec.get("enabled"):
        return False
    how = spec.get("value", "inline")
    figure_format = spec.get("figure_format", "retina")
    figure_format_ = f"InlineBackend.figure_format = '{figure_format}'"
    magic("matplotlib", how)
    magic("config", figure_format_)
    return True


@magic_handler
def magic_autoreload(helper, spec: Dict) -> bool:
    magic = helper.ipy.run_line_magic
    magics_manager = helper.ipy.magics_manager
    value = spec.get("value", "all")
    if isinstance(magics_manager, MagicsManager):
        if "autoreload" not in magics_manager.magics["line"]:
            magic("load_ext", "autoreload")
        magic("autoreload", value)
        print(f"Extension autoreload is loaded and set to {value}.")
        return True
    else:
        return False


modules = [
    pyplot,
    scienceplots,
    copydf,
    seaborn,
    numpy,
    numexpr,
    numba,
    sympy,
    scipy,
    pandas,
]
magics = [magic_matplotlib, magic_autoreload]
