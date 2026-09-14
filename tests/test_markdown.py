import contextlib
from pathlib import Path

import pytest

from readme_renderer.markdown import render, variants


def expect_extra_warning() -> contextlib.nullcontext | pytest.WarningsRecorder:
    """Expect the missing-extra ``UserWarning`` only when it actually fires.

    ``render()`` warns that "Markdown renderers are not available"
    only when the optional ``md`` extra is not installed.
    When the extra is present the same calls run silently,
    so an unconditional ``pytest.warns`` would fail there.
    Returning ``pytest.warns`` only on the ``noextra`` platform
    keeps expected warnings out of the test summary on both,
    and asserts the warning when it is genuinely expected.
    """
    if variants:
        return contextlib.nullcontext()
    return pytest.warns(
        UserWarning, match="Markdown renderers are not available"
    )


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
    with expect_extra_warning():
        assert render('Hello', variant="InvalidVariant") is None
