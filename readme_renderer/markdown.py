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

import re

import cmarkgfm
import pygments
import pygments.lexers
import pygments.formatters
from six.moves import html_parser

from .clean import clean


variants = {
    "GFM": cmarkgfm.github_flavored_markdown_to_html,
    "CommonMark": cmarkgfm.markdown_to_html,
}


def render(raw, variant="GFM", **kwargs):
    renderer = variants.get(variant)

    if not renderer:
        return None

    rendered = renderer(raw)

    if not rendered:
        return None

    highlighted = _highlight(rendered)
    cleaned = clean(highlighted)
    return cleaned


def _highlight(html):
    """Syntax-highlights HTML-rendered Markdown.

    Plucks sections to highlight that conform the the GitHub fenced code info
    string as defined at https://github.github.com/gfm/#info-string.

    Args:
        html (str): The rendered HTML.

    Returns:
        str: The HTML with Pygments syntax highlighting applied to all code
            blocks.
    """

    formatter = pygments.formatters.HtmlFormatter(nowrap=True)

    code_expr = re.compile(
        r'<pre><code class="language-(?P<lang>.+?)">(?P<code>.+?)'
        r'</code></pre>', re.DOTALL)

    def replacer(match):
        try:
            lexer = pygments.lexers.get_lexer_by_name(match.group('lang'))
        except ValueError:
            lexer = pygments.lexers.TextLexer()

        code = match.group('code')

        # Decode html entities in the code. cmark tries to be helpful and
        # translate '"' to '&quot;', but it confuses pygments. Pygments will
        # escape any html entities when re-writing the code, and we run
        # everything through bleach after.
        code = html_parser.HTMLParser().unescape(code)

        highlighted = pygments.highlight(code, lexer, formatter)

        return '<pre>{}</pre>'.format(highlighted)

    result = code_expr.sub(replacer, html)

    return result
