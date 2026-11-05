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

import re
import warnings
from collections.abc import Callable
from html import unescape
from re import Match
from typing import Any
from urllib.parse import unquote

import pygments
import pygments.formatters
import pygments.lexers

from .clean import clean

_EXTRA_WARNING = (
    "Markdown renderers are not available. "
    "Install 'readme_renderer[md]' to enable Markdown rendering."
)

# Prefix for header IDs to avoid conflicts with page elements.
# Must match the value passed to comrak's header_id_prefix option.
_HEADER_ID_PREFIX = "user-content-"

try:
    import comrak

    gfm_extension_options = comrak.ExtensionOptions()
    gfm_extension_options.alerts = True
    gfm_extension_options.autolink = True
    gfm_extension_options.footnotes = True
    gfm_extension_options.header_id_prefix = _HEADER_ID_PREFIX
    gfm_extension_options.shortcodes = True
    gfm_extension_options.strikethrough = True
    gfm_extension_options.table = True
    gfm_extension_options.tagfilter = True
    gfm_extension_options.tasklist = True

    common_render_options = comrak.RenderOptions()
    common_render_options.unsafe_ = True  # handled by nh3
    common_render_options.alert_style = comrak.AlertStyle.Semantic

    variants: dict[str, Callable[[str], str]] = {
        "GFM": lambda raw: comrak.render_markdown(
            raw,
            extension_options=gfm_extension_options,
            render_options=common_render_options,
        ),
        "CommonMark": lambda raw: comrak.render_markdown(
            raw,
            render_options=common_render_options,
        ),
    }

except ImportError:
    warnings.warn(_EXTRA_WARNING)
    variants = {}


def render(
    raw: str,
    variant: str = "GFM",
    **kwargs: Any
) -> str | None:
    if not variants:
        warnings.warn(_EXTRA_WARNING)
        return None

    renderer = variants.get(variant)

    if not renderer:
        return None

    rendered = renderer(raw)

    if not rendered:
        return None

    # GFM uses header_id_prefix which prefixes generated IDs. We need to also
    # prefix relative links so they correctly point to those IDs.
    if variant == "GFM":
        rendered = _prefix_relative_links(rendered, _HEADER_ID_PREFIX)

    highlighted = _highlight(rendered)
    cleaned = clean(highlighted)
    return cleaned


def _highlight(html: str) -> str:
    """Syntax-highlights HTML-rendered Markdown.

    Plucks sections to highlight that conform to the GitHub fenced code info
    string as defined at https://github.github.com/gfm/#info-string.

    Args:
        html (str): The rendered HTML.

    Returns:
        str: The HTML with Pygments syntax highlighting applied to all code
            blocks.
    """

    formatter = pygments.formatters.HtmlFormatter(nowrap=True)

    code_expr = re.compile(
        # cmarkgfm<0.6.0: <pre><code class="language-python">print('hello')</code></pre>
        # cmarkgfm>=0.6.0: <pre lang="python"><code>print('hello')</code></pre>
        r'(<pre>(?P<in_code><code) class="language-|<pre lang=")(?P<lang>[^"]+?)">'
        '(?(in_code)|<code>)(?P<code>.+?)'
        r'</code></pre>', re.DOTALL)

    def replacer(match: Match[Any]) -> str:
        try:
            lang = match.group('lang')
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except ValueError:
            lexer = pygments.lexers.TextLexer()

        code = match.group('code')

        # Decode html entities in the code. cmark tries to be helpful and
        # translate '"' to '&quot;', but it confuses pygments. Pygments will
        # escape any html entities when re-writing the code, and we run
        # everything through bleach after.
        code = unescape(code)

        highlighted = pygments.highlight(code, lexer, formatter)

        return f'<pre lang="{lang}">{highlighted}</pre>'

    result = code_expr.sub(replacer, html)

    return result


def _prefix_relative_links(html: str, prefix: str) -> str:
    """Add prefix to relative anchor links to match prefixed header IDs.

    When header_id_prefix is set in comrak, the generated id attributes get the
    prefix, but href attributes pointing to anchors do not. This function
    rewrites relative links (href="#...") to include the prefix so they
    correctly link to the prefixed header IDs.

    Note: Generated footnote links are excluded since comrak does not prefix
    footnote IDs with header_id_prefix. Ordinary links starting with fn-* or
    fnref-* can still point to headings.

    Args:
        html: The rendered HTML.
        prefix: The prefix to add to relative links.

    Returns:
        The HTML with prefixed relative anchor links.
    """
    heading_ids = {
        unescape(value) for value in re.findall(r'<h[1-6] id="([^"]+)"', html)
    }

    def replacer(match: Match[str]) -> str:
        if match.group("footnote"):
            return match.group(0)
        anchor = match.group("anchor")
        target = prefix + unquote(unescape(anchor))
        # Preserve manual footnote links unless they target a heading.
        if anchor.startswith(("fn-", "fnref-")) and target not in heading_ids:
            return match.group(0)
        return f'href="#{prefix}{anchor}"'

    # Consume whole attributes, so marker words in titles are not attributes.
    attribute = (
        r'''[^\s"'<>/=]+'''
        r'''(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))?'''
    )
    return re.sub(
        rf'(?P<footnote><a(?:\s+{attribute})*'
        r'\s+data-footnote-(?:ref|backref)(?=[\s>])'
        rf'(?:\s+{attribute})*\s*>)'
        r'|href="#(?P<anchor>[^"]+)"',
        replacer,
        html,
    )
