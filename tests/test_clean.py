import pytest

from readme_renderer import clean


def test_invalid_link():
    assert clean.clean('<a href="http://exam](ple.com">foo</a>') == "<a>foo</a>"


@pytest.mark.parametrize(
    "tag, name, value, expected",
    [
        ("form", "align", "left", False),  # form doesn't allow attributes
        ("h1", "align", "left", True),  # h1 allows align attribute
        ("h1", "class", "align-left", False),  # h1 doesn't allow class
        ("img", "onerror", "alert()", False),  # img doesn't onerror attribute
        ("img", "class", "something", False),  # img allows class but not this one
        ("img", "class", "align-left", True),  # img allows this class
        ("img", "id", "some-id", True),  # everything allows id
        ("form", "id", "some-id", True),  # everything allows id
    ]
)
def test_is_attributes_allowed(tag, name, value, expected):
    assert clean.is_attributes_allowed(tag, name, value) == expected
