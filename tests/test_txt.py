from pathlib import Path

import pytest

from readme_renderer.txt import render


@pytest.mark.parametrize(
    ("txt_filename", "html_filename"),
    [
        (pytest.param(fn, fn.with_suffix(".html"), id=fn.name))
        for fn in Path(__file__).parent.glob("fixtures/test_*.txt")
    ],
)
def test_txt_fixtures(txt_filename, html_filename):
    # Get our Markup
    with open(txt_filename, encoding='utf-8') as f:
        txt_markup = f.read()

    # Get our expected
    with open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    out = render(txt_markup)

    assert out.strip() == expected.strip()
