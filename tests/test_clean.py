from readme_renderer.clean import clean


def test_invalid_link():
    assert (
        clean('<a href="http://exam](ple.com">foo</a>') == '<a rel="nofollow">foo</a>'
    )


def test_invalid_input_controls_are_removed():
    assert (
        clean(
            '<input type="submit">'
            '<input type="text">'
            '<input type="checkbox" checked>'
            '<input type="checkbox">'
        ) == ""
    )


def test_disabled_checkbox_inputs_are_allowed():
    assert clean(
        '<input type="checkbox" disabled><input type="checkbox" checked disabled>'
    ) == (
        '<input type="checkbox" disabled="">'
        '<input type="checkbox" checked="" disabled="">'
    )
