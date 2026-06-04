from readme_renderer.clean import clean


def test_invalid_link():
    assert clean(
        '<a href="http://exam](ple.com">foo</a>'
    ) == '<a rel="nofollow">foo</a>'


def test_custom_tags_are_respected():
    assert clean(
        "<p>plain text</p><br><strong>bold text</strong>",
        tags={"br"},
    ) == "plain text<br>bold text"


def test_custom_attributes_are_respected():
    assert clean(
        '<img src="https://example.com/image.png" alt="image" width="100">',
        attributes={"img": {"alt"}},
    ) == '<img alt="image">'


def test_active_input_controls_are_disabled():
    # Every input is forced disabled, and non-checkbox types are dropped, so
    # nothing interactive survives.
    assert clean(
        '<input type="submit">'
        '<input type="text">'
        '<input type="checkbox" checked>'
        '<input type="checkbox">'
    ) == (
        '<input disabled="">'
        '<input disabled="">'
        '<input type="checkbox" checked="" disabled="">'
        '<input type="checkbox" disabled="">'
    )


def test_disabled_checkbox_inputs_are_preserved():
    assert clean(
        '<input type="checkbox" disabled><input type="checkbox" checked disabled>'
    ) == (
        '<input type="checkbox" disabled="">'
        '<input type="checkbox" checked="" disabled="">'
    )
