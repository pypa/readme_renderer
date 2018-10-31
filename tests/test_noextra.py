import pytest

from readme_renderer.markdown import render, variants


@pytest.mark.skipif(variants, reason="Extra is installed")
@pytest.mark.parametrize("variant", ('GFM', 'CommonMark'))
def test_no_extra(variant):
    with pytest.warns(UserWarning) as warnings:
        assert render('Hello', variant=variant) is None
    assert len(warnings) == 1
    assert warnings[0].message.args[0] == (
        "Markdown renderers are not available. "
        "Install 'readme_renderer[md]' to enable Markdown rendering."
    )
