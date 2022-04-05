import urllib
from pathlib import Path
from typing import TYPE_CHECKING

import dominate.tags as dt

if TYPE_CHECKING:
    from htmlreport import HTMLReport


def embed_js_in_report(rep: "HTMLReport") -> "HTMLReport":
    rep.document.head.add(dt.script(src="bootstrap-4.3.1.js"))
    rep.document.head.add(dt.script(src="jquery-3.3.1.js"))
    rep.document.head.add(dt.script(src="plotly-1.58.5.js"))
    rep.document.head.add(dt.script(src="bootstrap-4.3.1.css", rel="stylesheet"))
    return rep


def read_js(file_name):
    with open(Path(__file__).parent / file_name) as file:
        return file.read()
