import io
import glob
import os

import pytest

from readme_renderer.markdown import render, variants


MD_FIXTURES = [
    (fn, os.path.splitext(fn)[0] + ".html", variant)
    for variant in variants
    for fn in glob.iglob(
        os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "test_" + variant + "*.md"
        )
    )
]


@pytest.mark.parametrize(
    ("md_filename", "html_filename", "variant"),
    MD_FIXTURES,
)
def test_md_fixtures(md_filename, html_filename, variant):
    # Get our Markup
    with io.open(md_filename, encoding='utf-8') as f:
        md_markup = f.read()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    assert render(md_markup, variant=variant) == expected


def test_missing_variant():
    assert render('Hello', variant="InvalidVariant") is None
