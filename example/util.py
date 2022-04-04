import urllib
from typing import TYPE_CHECKING

import dominate.tags as dt

if TYPE_CHECKING:
    from htmlreport import HTMLReport


def embed_js_in_report(rep: "HTMLReport") -> "HTMLReport":
    target_url = [
        "https://cdn.plot.ly/plotly-latest.min.js",
        "https://code.jquery.com/jquery-3.3.1.slim.min.js",
        "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
    ]
    for url in target_url:
        rep.add(dt.script(read_js(target_url=url)))
    return rep


def read_js(target_url):
    file = urllib.request.urlopen(target_url)
    return file.read()
