# Copyright 2014 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from html.parser import HTMLParser

import nh3


ALLOWED_TAGS = {
    # Bleach Defaults
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol",
    "strong", "ul",

    # Custom Additions
    "br", "caption", "cite", "col", "colgroup", "dd", "del", "details", "div",
    "dl", "dt", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img", "p", "pre",
    "span", "sub", "summary", "sup", "table", "tbody", "td", "th", "thead",
    "tr", "tt", "kbd", "var", "input", "section", "aside", "nav", "figure",
    "figcaption", "picture",
}

ALLOWED_ATTRIBUTES = {
    # Bleach Defaults
    "a": {"href", "title"},
    "abbr": {"title"},
    "acronym": {"title"},

    # Custom Additions
    "*": {"id"},
    "hr": {"class"},
    "img": {"src", "width", "height", "alt", "align", "class"},
    "span": {"class"},
    "th": {"align", "class"},
    "td": {"align", "colspan", "rowspan"},
    "div": {"align", "class"},
    "h1": {"align"},
    "h2": {"align"},
    "h3": {"align"},
    "h4": {"align"},
    "h5": {"align"},
    "h6": {"align"},
    "code": {"class"},
    "p": {"align", "class"},
    "pre": {"lang"},
    "ol": {"start"},
    "input": {"type", "checked", "disabled"},
    "aside": {"class"},
    "dd": {"class"},
    "dl": {"class"},
    "dt": {"class"},
    "ul": {"class"},
    "nav": {"class"},
    "figure": {"class"},
}


class _InvalidInputFilter(HTMLParser):
    """Collect sanitized input start tags that are not GFM task-list checkboxes."""

    def __init__(self, html: str) -> None:
        super().__init__(convert_charrefs=False)
        self.invalid_spans: list[tuple[int, int]] = []
        self._line_offsets = _line_offsets(html)

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self._record_invalid_input(tag, attrs)

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self._record_invalid_input(tag, attrs)

    def _record_invalid_input(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag != "input" or _valid_input_attrs(attrs):
            return

        start_tag = self.get_starttag_text()
        if start_tag is None:
            return

        line, offset = self.getpos()
        start = self._line_offsets[line - 1] + offset
        self.invalid_spans.append((start, start + len(start_tag)))


def _line_offsets(html: str) -> list[int]:
    """Return absolute offsets for the start of each line in an HTML fragment."""

    offsets = [0]
    for index, char in enumerate(html):
        if char == "\n":
            offsets.append(index + 1)
    return offsets


def _valid_input_attrs(attrs: list[tuple[str, str | None]]) -> bool:
    """Return whether an input tag has only the allowed task-list attributes."""

    attr_map = dict(attrs)
    if attr_map.get("type") != "checkbox":
        return False
    if "disabled" not in attr_map:
        return False
    return set(attr_map) <= {"type", "checked", "disabled"}


def _remove_invalid_inputs(html: str) -> str:
    """Strip input tags that are not disabled checkbox task-list controls."""

    parser = _InvalidInputFilter(html)
    parser.feed(html)

    cleaned = html
    for start, end in reversed(parser.invalid_spans):
        cleaned = cleaned[:start] + cleaned[end:]
    return cleaned


def clean(
    html: str,
    tags: set[str] | None = None,
    attributes: dict[str, set[str]] | None = None,
) -> str | None:
    if tags is None:
        tags = ALLOWED_TAGS
    if attributes is None:
        attributes = ALLOWED_ATTRIBUTES

    try:
        cleaned = nh3.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            link_rel="nofollow",
            url_schemes={"http", "https", "mailto"},
        )
    except ValueError:
        return None
    return _remove_invalid_inputs(cleaned)
