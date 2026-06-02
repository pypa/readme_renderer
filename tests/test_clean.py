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
