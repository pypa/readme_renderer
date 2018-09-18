from readme_renderer.clean import clean


def test_invalid_link():
    assert clean('<a href="http://exam](ple.com">foo</a>') == "<a>foo</a>"


def test_css_sanitizer():
    r = clean("<span class='foo'><img class='align-right bar'></span>")
    assert r == '<span><img class="align-right"></span>'
