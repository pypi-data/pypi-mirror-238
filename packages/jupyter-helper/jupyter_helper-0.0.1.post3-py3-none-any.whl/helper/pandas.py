from typing import List

from IPython.display import display_html
from pandas import DataFrame

from .util import warn_html


class PandasTricks:
    def __init__(self, support_html: bool) -> None:
        self.support_html = support_html

    @warn_html
    def display_side_by_side(self, *dfs: List[DataFrame]) -> None:
        html_str = ""
        for df in dfs:
            if not isinstance(df, DataFrame):
                raise TypeError("Must be DataFrame")
            html_str += df.to_html()
        display_html(
            html_str.replace("table", 'table style="display:inline"'),
            raw=True,
        )
