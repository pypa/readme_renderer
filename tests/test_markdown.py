import io
import glob
import os

import pytest

from readme_renderer.markdown import render


@pytest.mark.parametrize(
    ("md_filename", "html_filename"),
    [
        (fn, os.path.splitext(fn)[0] + ".html")
        for fn in glob.glob(
            os.path.join(os.path.dirname(__file__), "fixtures", "test_*.md")
        )
    ],
)
def test_md_fixtures(md_filename, html_filename):
    # Get our Markup
    with io.open(md_filename, encoding='utf-8') as f:
        md_markup = f.read()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    assert render(md_markup) == expected
