from readme_renderer.clean import clean


def test_invalid_link():
    assert clean('<a href="http://exam](ple.com">foo</a>') == "<a>foo</a>"
