import plotly.express as px
from dominate import tags as dt

from htmlreport.tabby import Tabby

# actual left, expected right


def test_tabby():
    keys = ["A", "C", "E"]
    tab = Tabby(keys=keys)
    assert list(tab.keys()) == keys


def test_nav_bar_to_dom_tag():
    keys_act = ["A", "C", "E"]
    tab = Tabby(keys=keys_act, uid="abc")
    act = tab._nav_bar_to_dom_tag()

    exp = dt.div(cls="nav nav-tabs nav-fill", id="tabby-abc-nav", role="tablist")
    for key in keys_act:
        exp.add(
            dt.a(
                key,
                aria_controls=f"tabby-abc-content-{key.lower()}",
                aria_selected=f"{'true' if key == 'A' else 'false'}",
                cls=f"nav-item nav-link{' active' if key == 'A' else ''}",
                data_toggle="tab",
                href=f"#tabby-abc-content-{key.lower()}",
                id=f"tabby-abc-nav-{key.lower()}",
                role="tab",
            )
        )
    assert act.render() == exp.render()


def test_content_to_dom_tag():
    keys_act = ["A", "C"]
    objs_act = [dt.p("Hello"), [dt.div(style="flex", id="c-div"), dt.h1("Hello world")]]
    tab = Tabby(keys=["A", "C"], uid="abc")
    tab.add(key=keys_act[0], obj=objs_act[0])
    tab.add(key=keys_act[1], obj=objs_act[1][0])
    tab.add(key=keys_act[1], obj=objs_act[1][1])
    act = tab._content_to_dom_tag()

    exp = dt.div(cls="tab-content", id="tabby-abc-con")
    for key, objects in zip(keys_act, objs_act):
        content_key = dt.div(
            aria_labelledby=f"tabby-abc-nav-{key.lower()}",
            cls=f"tab-pane fade show{' active' if key == 'A' else ''}",
            id=f"tabby-abc-content-{key.lower()}",
            role="tabpanel",
        )
        if len(objects) == 1:
            content_key.add(dt.div(objects))
        else:
            for obj in objects:
                content_key.add(dt.div(obj))
        exp.add(content_key)

    assert act.render() == exp.render()


def test_add_para():
    tab = Tabby(keys=["A", "C"], uid="abc")
    assert not tab.data["A"]
    tab.add_para(key="A", content="Hello world")
    assert tab.data["A"]
    assert isinstance(tab.data["A"][0], dt.p)


def test_to_dom_tag():
    tab = Tabby(keys=["A", "C"], uid="abc")
    assert not tab.data["A"]
    tab.add(key="A", obj=dt.p("Hello world 1"))
    assert tab.data["A"]
    assert not tab.data["C"]
    tab.add(key="C", obj=dt.p("Hello world 2"))
    tab.add(key="C", obj=dt.p("Hello world 3"))
    assert len(tab.data["C"]) == 2


def test_keys():
    tab = Tabby(keys=[2, 3])
    tab.add(key=1, obj=dt.h1("Hello world"))
    assert tab.keys() == ["2", "3", "1"]


def test_add_pd_df(generate_mini_data):
    tab = Tabby()
    assert not tab.data["A"]
    tab.add(key="A", obj=generate_mini_data)
    assert tab.data["A"]
    assert "table" in tab.data["A"][0].text


def test_add_pd_styler(generate_mini_data):
    tab = Tabby()
    assert not tab.data["A"]
    tab.add(key="A", obj=generate_mini_data.style)
    assert tab.data["A"]
    assert "table" in tab.data["A"][0].text


def test_add_plotly_figure(generate_mini_data):
    tab = Tabby()
    assert not tab.data["A"]
    tab.add(key="A", obj=px.scatter(generate_mini_data, x="A", y="B"))
    assert tab.data["A"]
    assert "plotly-graph-div" in tab.data["A"][0].text


def test_add_matplotlib_figure(matplotlib_figure):
    tab = Tabby()
    assert not tab.data["A"]
    tab.add(key="A", obj=matplotlib_figure)
    assert tab.data["A"]
    assert "data:image/png;base64" in tab.data["A"][0].text
