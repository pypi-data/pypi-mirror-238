#!/usr/bin/env python3

from typing import Callable

from IPython.core.interactiveshell import InteractiveShell
from IPython.display import Markdown, display


class Misc:
    def __init__(self, ipy: InteractiveShell, support_html: bool) -> None:
        self.support_html = support_html
        self.ipy = ipy

    def rescue_func(self, function: Callable) -> None:
        """
        Rescue the code that it's cell been deleted but still running the notebook.
        Via Robin's Blog: http://blog.rtwilson.com/how-to-rescue-lost-code-from-a-jupyteripython-notebook/
        """
        import inspect

        self.ipy.set_next_input("".join(inspect.getsourcelines(function)[0]))

    def printmd(self, string, color=None):
        """
        https://github.com/NirantK/best-of-jupyter
        Including markdown in your code’s output is very useful. Use this to highlight parameters, performance notes and so on. This enables colors, Bold, etc.
        """
        colorstr = "<span style='color:{}'>{}</span>".format(color, string)
        display(Markdown(colorstr))
