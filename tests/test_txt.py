import io
import glob
import os.path

import pytest

from readme_renderer.txt import render


@pytest.mark.parametrize(
    ("txt_filename", "html_filename"),
    [
        (fn, os.path.splitext(fn)[0] + ".html")
        for fn in glob.glob(
            os.path.join(os.path.dirname(__file__), "fixtures", "test_*.txt")
        )
    ],
)
def test_txt_fixtures(txt_filename, html_filename):
    # Get our Markup
    with io.open(txt_filename, encoding='utf-8') as f:
        txt_markup = f.read()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    out = render(txt_markup)

    assert out.strip() == expected.strip()
