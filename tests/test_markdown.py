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


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
def test_extension_options_are_per_call():
    import comrak

    options = comrak.ExtensionOptions()
    options.shortcodes = False
    assert render(':tada:', extension_options=options) == '<p>:tada:</p>\n'
    assert render(':tada:') == '<p>🎉</p>\n'
    assert options.shortcodes is False


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
@pytest.mark.parametrize('variant', ['GFM', 'CommonMark'])
@pytest.mark.parametrize('prefix', ['custom-', ''])
def test_extension_header_prefix_matches_links(variant, prefix):
    import comrak

    options = comrak.ExtensionOptions()
    options.header_id_prefix = prefix
    result = render('# Title\n\n[Jump](#title)', variant=variant,
                    extension_options=options)
    assert f'id="{prefix}title"' in result
    assert f'href="#{prefix}title"' in result


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
@pytest.mark.parametrize('variant', ['GFM', 'CommonMark'])
def test_render_options_are_per_call(variant):
    import comrak

    options = comrak.RenderOptions()
    options.hardbreaks = True
    assert render('one\ntwo', variant=variant, render_options=options) == (
        '<p>one<br>\ntwo</p>\n'
    )
    assert render('one\ntwo', variant=variant) == '<p>one\ntwo</p>\n'


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
def test_custom_options_still_sanitize_html():
    import comrak

    options = comrak.RenderOptions()
    options.unsafe_ = True
    result = render('<script>alert(1)</script>\n\nHello',
                    render_options=options)
    assert '<script' not in result
    assert '<p>Hello</p>' in result


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
def test_extension_options_can_disable_header_ids():
    import comrak

    options = comrak.ExtensionOptions()
    result = render('# Title\n\n[Jump](#title)', extension_options=options)
    assert '<h1>Title</h1>' in result
    assert 'href="#title"' in result


@pytest.mark.skipif(not variants, reason="Markdown extra is not installed")
def test_custom_prefix_does_not_change_footnote_links():
    import comrak

    options = comrak.ExtensionOptions()
    options.header_id_prefix = 'custom-'
    options.footnotes = True
    result = render('Text[^1]\n\n[^1]: Note', extension_options=options)
    assert 'href="#fn-1"' in result
    assert 'href="#custom-fn-' not in result
