from pathlib import Path

import pytest

from readme_renderer.markdown import render, variants


@pytest.mark.parametrize(
    ("md_filename", "html_filename", "variant"),
    [
        (pytest.param(fn, fn.with_suffix(".html"), variant, id=fn.name))
        for variant in variants
        for fn in Path(__file__).parent.glob(f"fixtures/test_{variant}*.md")
    ],
)
def test_md_fixtures(md_filename, html_filename, variant):
    # Get our Markup
    with open(md_filename, encoding='utf-8') as f:
        md_markup = f.read()

    # Get our expected
    with open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    assert render(md_markup, variant=variant) == expected


def test_missing_variant():
    assert render('Hello', variant="InvalidVariant") is None
