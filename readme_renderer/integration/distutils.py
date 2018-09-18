# Copyright 2015 Donald Stufft
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

import cgi
import io
import re
import sys
import webbrowser

import distutils.log
from distutils.command.check import check as _check
from distutils.core import Command
from tempfile import NamedTemporaryFile
import six

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import HtmlLexer

from ..rst import render


# Regular expression used to capture and reformat doctuils warnings into
# something that a human can understand. This is loosely borrowed from
# Sphinx: https://github.com/sphinx-doc/sphinx/blob
# /c35eb6fade7a3b4a6de4183d1dd4196f04a5edaf/sphinx/util/docutils.py#L199
_REPORT_RE = re.compile(
    r'^<string>:(?P<line>(?:\d+)?): '
    r'\((?P<level>DEBUG|INFO|WARNING|ERROR|SEVERE)/(\d+)?\) '
    r'(?P<message>.*)', re.DOTALL | re.MULTILINE)


RST_TYPE = 'text/x-rst'
MD_TYPE = 'text/markdown'
PLAIN_TYPE = 'text/plain'


@six.python_2_unicode_compatible
class _WarningStream(object):
    def __init__(self):
        self.output = io.StringIO()

    def write(self, text):
        matched = _REPORT_RE.search(text)

        if not matched:
            self.output.write(text)
            return

        self.output.write(
            u"line {line}: {level_text}: {message}\n".format(
                level_text=matched.group('level').capitalize(),
                line=matched.group('line'),
                message=matched.group('message').rstrip('\r\n')))

    def __str__(self):
        return self.output.getvalue()


class Check(_check):
    def check_restructuredtext(self):
        """
        Checks if the long string fields are reST-compliant.
        """
        data = self.distribution.get_long_description()
        content_type = getattr(
            self.distribution.metadata, 'long_description_content_type', None)

        if content_type:
            content_type, _ = cgi.parse_header(content_type)
            if content_type != 'text/x-rst':
                self.warn(
                    "Not checking long description content type '%s', this "
                    "command only checks 'text/x-rst'." % content_type)
                return

        # None or empty string should both trigger this branch.
        if not data or data == 'UNKNOWN':
            self.warn(
                "The project's long_description is either missing or empty.")
            return

        stream = _WarningStream()
        markup = render(data, stream=stream)

        if markup is None:
            self.warn(
                "The project's long_description has invalid markup which will "
                "not be rendered on PyPI. The following syntax errors were "
                "detected:\n%s" % stream)
            return

        self.announce(
            "The project's long description is valid RST.",
            level=distutils.log.INFO)


class RenderReadme(Command):

    """Render and display the long description as HTML."""
    description = ("render the long description as HTML")
    user_options = [("preview", None,
                     "Preview readme"),
                    ("no-color", None,
                     "Do not colorize..."),
                    ("style=", None,
                     "Pygments style to use to colorize HTML output.")]

    def initialize_options(self):
        self.preview = False
        self.no_color = False
        self.style = 'native'

    def finalize_options(self):
        pass

    def get_renderer(self):
        content_type = getattr(
            self.distribution.metadata, 'long_description_content_type', None)

        if content_type == RST_TYPE:
            from ..rst import render as rst_render
            return rst_render
        elif content_type == MD_TYPE:
            from ..markdown import render as md_render
            return md_render
        elif content_type == PLAIN_TYPE:
            from ..txt import render as txt_render
            return txt_render
        else:
            from ..rst import render as rst_render
            return rst_render

    def run(self):
        """Runs the command."""

        data = self.distribution.get_long_description()
        stream = io.StringIO()
        # TODO: this will only work for RST!!!
        render = self.get_renderer()
        markup = render(data, stream=stream)

        for line in stream.getvalue().splitlines():
            if line.startswith("<string>"):
                line = line[8:]
            self.warn(line)

        if markup is None:
            self.warn("Invalid markup which will not be rendered on PyPI.")

        if self.preview:
            with NamedTemporaryFile(
                prefix='render_readme_',
                suffix='.html',
                delete=False,
            ) as f:
                print('Writing readme to {0}'.format(f.name))
                f.write(markup.encode('utf-8'))

            webbrowser.open('file://' + f.name.replace('\\', '/'))
        else:
            if not self.no_color:
                lexer = HtmlLexer()
                formatter = Terminal256Formatter(style=self.style)
                markup = highlight(markup, lexer, formatter)
            sys.stdout.write(markup)
