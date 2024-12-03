from pathlib import Path

import plotly.express as px
import seaborn as sns

from example.util import embed_js_in_report
from htmlreport import HTMLReport, Tabby

iris = sns.load_dataset("iris")

# section 1: prepare data

data_summary = iris.head(5).style.format(precision=2)
data_summary.set_table_styles(
    [
        {"selector": "th.col_heading", "props": "text-align: center;"},
        {"selector": "th.col_heading.level0", "props": "font-size: 1.5em;"},
        {"selector": "td", "props": "text-align: center; font-weight: bold;"},
    ],
    overwrite=False,
)
data_summary.set_caption("The iris dataset").set_table_styles(
    [
        {
            "selector": "caption",
            "props": "caption-side: bottom; text-align: center; font-size:1.25em;",
        }
    ],
    overwrite=False,
)

keys = [str(ele) for ele in iris["species"].unique()]
tab_spec = Tabby(keys=keys)
var_to_display = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
for spec in keys:
    mask = iris["species"] == spec
    to_plot = iris.loc[mask, var_to_display]
    tab_spec.add(key=spec, obj=px.box(to_plot))
    tab_spec.add_para(
        key=spec,
        content="""Plots produced with Plotly reap all the benefits of Plotly's javascript. For example, check the 
        responsiveness of plots by resizing your window!""",
    )

# section 2: produce report

rep = HTMLReport(
    title="html-report: Example Report",
    default_header_size=3,
    default_section_width="70%",
)

rep = embed_js_in_report(rep=rep)

rep.add_section(id="summ")
rep.add_header(content="Data Overview", sec="summ")
rep.add_markdown(
    content="""Use of `add_section()` creates border around content later added to section.  
    The heading above, paragraph below and data below are added using `add_header()`, `add_para()` and `add()`, 
    respectively.""",
    sec="summ",
)
rep.add_para(
    content="The first 5 rows of the data to analyse:",
    sec="summ",
)
rep.add(data_summary, sec="summ")


rep.add_section(id="spec")
rep.add_header(content="Analysis of Species", sec="spec")
rep.add_markdown(
    content="Line breaks and emphasis in the descriptive content below is achieved with markdown style input.",
    sec="spec",
)
rep.add_markdown(
    content=f"""There are 3 species to analyse:  
<em>{keys[0]}</em>  
<em>{keys[1]}</em>  
<em>{keys[2]}</em>""",
    sec="spec",
)
rep.add_para(
    content="See use of Tabby below:",
    sec="spec",
)
rep.add(obj=tab_spec, sec="spec")

output = rep.to_html()  # output as str
rep.save(
    filepath=Path(__file__).parent / "report.html", open_browser=True
)  # output as file
