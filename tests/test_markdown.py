import io
import glob
import os

import cmarkgfm
import pytest

from readme_renderer.markdown import render, variants


MD_FIXTURES = [
    (fn, os.path.splitext(fn)[0] + ".html", variant)
    for variant in variants
    for fn in glob.glob(
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
        md_markup = f.read().strip()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read().strip()

    assert render(md_markup, variant=variant).strip() == expected


def test_missing_variant():
    assert render('Hello', variant="InvalidVariant") is None


def test_cmarkgfm_is_preferred():
    assert variants['CommonMark'] is cmarkgfm.markdown_to_html
