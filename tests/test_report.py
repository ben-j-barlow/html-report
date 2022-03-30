from pathlib import Path

import dominate
import dominate.tags as dt
import plotly.express as px
import pytest

from htmlreport.report import HTMLReport


def test_HTMLReport_dominate():
    rep = HTMLReport()
    assert isinstance(rep.document, dominate.document)


def test_HTMLReport_title():
    rep = HTMLReport(title="Test report")
    assert rep.document.head.children
    assert isinstance(rep.document.head.children[0], dt.title)


def test_add_header():
    rep = HTMLReport()
    assert not rep.document.body.children
    rep.add_header(content="Test Heading", size=6)
    assert rep.document.body.children
    assert isinstance(rep.document.body[0], dt.h6)
    assert "Test Heading" == rep.document.body[0].children[0]


def test_add_para():
    rep = HTMLReport()
    assert not rep.document.body.children
    rep.add_para(content="Test para")
    assert rep.document.body.children
    assert isinstance(rep.document.body[0], dt.p)
    assert "Test para" == rep.document.body[0].children[0]


def test_save_filepath_pathlib(tmpdir):
    rep = HTMLReport()
    filepath = Path(tmpdir.join("tmp.html"))
    assert not filepath.is_file()
    rep.save(filepath=filepath, open_browser=False)
    assert filepath.is_file()


def test_save_filepath_str(tmpdir):
    rep = HTMLReport()
    filepath = tmpdir.join("tmp.html")
    assert not Path(filepath).is_file()
    rep.save(filepath=filepath, open_browser=False)
    assert Path(filepath).is_file()


def test_add_markdown():
    rep = HTMLReport()
    rep.add_markdown(
        """
# Hello world

## Step 1
### Step 2
* item 1
* item 2

Visit [the tutorials page](https://www.digitalocean.com/community/tutorials) for more tutorials!
"""
    )
    actual = rep.document.body[0]
    assert '<a href="https://www.digitalocean.com/community/tutorials">' in actual.text
    assert "<ul>" in actual.text
    assert "<h1>" in actual.text
    assert "<li>" in actual.text


def test_add_section():
    rep = HTMLReport()
    assert not rep.section
    assert isinstance(rep.section, dict)
    rep.add_section(id="my_sec")
    assert rep.section
    assert rep.section["my_sec"]
    assert isinstance(rep.section["my_sec"]["div"], dt.div)


def test_ref_section_before_created():
    rep = HTMLReport()
    assert not rep.section
    with pytest.raises(RuntimeError):
        rep.add_header(content="Hello world", sec="my_sec")


def test_set_section_width():
    rep = HTMLReport()
    rep.add_section(id="my_sec", width="50%")
    assert "width: 50%" in rep.section["my_sec"]["div"]["style"]


def test_handle_section():
    rep = HTMLReport()
    rep.add_section(id="my_sec")
    assert not rep.section["my_sec"]["div"].children
    rep.add_header(content="Header added to section", size=4, sec="my_sec")
    assert rep.section["my_sec"]["div"].children
    rep.add_header(content="Header not added to section", size=4)
    assert len(rep.section["my_sec"]["div"].children) == 1


def test_add_pd_df(generate_mini_data):
    rep = HTMLReport()
    rep.add(generate_mini_data)
    assert rep.document.body[0]
    assert "table" in rep.document.body[0].text


def test_add_pd_styler(generate_mini_data):
    rep = HTMLReport()
    rep.add(generate_mini_data.style)
    assert rep.document.body[0]
    assert "table" in rep.document.body[0].text


def test_add_plotly_figure(generate_mini_data):
    rep = HTMLReport()
    rep.add(obj=px.scatter(generate_mini_data, x="A", y="B"))
    assert rep.document.body[0]
    assert "plotly-graph-div" in rep.document.body[0].text
