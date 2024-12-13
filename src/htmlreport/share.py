from typing import TYPE_CHECKING, Union

import dominate.tags as dt

from htmlreport.helper import get_mpl_plot_as_base64

if TYPE_CHECKING:
    from matplotlib.pyplot import Figure as MatplotlibFigure
    from pandas import DataFrame
    from pandas.io.formats.style import Styler
    from plotly.graph_objects import Figure as PlotlyFigure


def _add_pandas_dataframe(obj: "DataFrame") -> str:
    return _add_pandas_styler(obj.style)


def _add_pandas_styler(obj: "Styler") -> str:
    html = obj.to_html()
    html = html.replace("\\n", "<br>")
    return html


def _add_plotly_figure(plot: "PlotlyFigure") -> str:
    html = plot.to_html(
        include_plotlyjs=False,
        full_html=False,
        include_mathjax=False,
        validate=True,
        config={"responsive": True},
    )
    return html


def _add_matplotlib_figure(plot: "MatplotlibFigure") -> str:
    return f'<img src="data:image/png;base64,{get_mpl_plot_as_base64(fig=plot)}">'


def _add_header(
    size: int, content: str
) -> Union[dt.h1, dt.h2, dt.h3, dt.h4, dt.h5, dt.h6]:
    if not 1 <= size <= 6:
        raise ValueError("size must take value 1, 2, 3, 4, 5 or 6")
    return getattr(dt, f"h{size}")(content)
