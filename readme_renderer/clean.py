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
from __future__ import absolute_import, division, print_function

import functools

import bleach
import bleach.callbacks
import bleach.linkifier
import bleach.sanitizer
import html5lib.filters.base
import pygments.token


ALLOWED_TAGS = [
    # Bleach Defaults
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol",
    "strong", "ul",

    # Custom Additions
    "br", "caption", "cite", "col", "colgroup", "dd", "del", "details", "div",
    "dl", "dt", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img", "p", "pre",
    "span", "sub", "summary", "sup", "table", "tbody", "td", "th", "thead",
    "tr", "tt", "kbd", "var",
]

ALLOWED_ATTRIBUTES = {
    # Bleach Defaults
    "a": ["href", "title"],
    "abbr": ["title"],
    "acronym": ["title"],

    # Custom Additions
    "*": ["id"],
    "hr": ["class"],
    "img": ["src", "width", "height", "alt", "align", "class", "style"],
    "span": ["class"],
    "th": ["align"],
    "td": ["align"],
    "code": ["class"],
    "p": ["align"],
}

ALLOWED_STYLES = [
    "width", "height",
]

ALLOWED_CLASSES = {
    "img": ["align-left", "align-center", "align-right"],
    "span": [c for c in pygments.token.STANDARD_TYPES.values() if c],
}


class _CSSClassFilter(html5lib.filters.base.Filter):
    def __init__(self, *args, allowed_classes=None, **kwargs):
        super().__init__(*args, **kwargs)

        if allowed_classes is None:
            allowed_classes = {}
        self.allowed_classes = allowed_classes

    def __iter__(self):
        for token in super().__iter__():
            token = self.sanitize_token(token)
            if token:
                yield token

    def sanitize_token(self, token):
        if token["type"] in {"StartTag", "EndTag", "EmptyTag"}:
            name = token["name"]

            if "data" in token:
                attrs = token["data"]

                if (None, "class") in attrs:
                    new_classes = self.sanitize_css_classes(
                        name,
                        attrs[(None, "class")]
                    )

                    if new_classes:
                        attrs[(None, "class")] = new_classes
                    else:
                        del attrs[(None, "class")]

                token["data"] = attrs

        return token

    def sanitize_css_classes(self, name, classes):
        classes = classes.split()
        allowed = set(self.allowed_classes.get(name, []))
        classes = sorted(set(classes) & allowed)
        return " ".join(classes)


def clean(html, tags=None, attributes=None, styles=None, classes=None):
    if tags is None:
        tags = ALLOWED_TAGS
    if attributes is None:
        attributes = ALLOWED_ATTRIBUTES
    if styles is None:
        styles = ALLOWED_STYLES
    if classes is None:
        classes = ALLOWED_CLASSES

    # Clean the output using Bleach
    cleaner = bleach.sanitizer.Cleaner(
        tags=tags,
        attributes=attributes,
        styles=styles,
        filters=[
            # Bleach by default doesn't allow whitelisting what CSS classes
            # are available to be used, so we'll override that behavior with
            # our own filter which does.
            functools.partial(_CSSClassFilter, allowed_classes=classes),
            # Bleach Linkify makes it easy to modify links, however, we will
            # not be using it to create additional links.
            functools.partial(
                bleach.linkifier.LinkifyFilter,
                callbacks=[
                    lambda attrs, new: attrs if not new else None,
                    bleach.callbacks.nofollow,
                ],
                skip_tags=["pre"],
                parse_email=False,
            ),
        ],
    )
    try:
        cleaned = cleaner.clean(html)
        return cleaned
    except ValueError:
        return None
