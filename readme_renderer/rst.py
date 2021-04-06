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

import io

from docutils import utils
from docutils.core import publish_parts
from docutils.writers.html4css1 import HTMLTranslator, Writer
from docutils.utils import SystemMessage

from .clean import clean


def extract_extension_options(field_list, option_spec):
    """
    Overrides `utils.extract_extension_options` and inlines
    `utils.assemble_option_dict` to make it ignore unknown options passed to
    directives (i.e. ``:caption:`` for ``.. code-block:``).
    """

    dropped = set()
    options = {}
    for name, value in utils.extract_options(field_list):
        convertor = option_spec.get(name)
        if name in options or name in dropped:
            raise utils.DuplicateOptionError('duplicate option "%s"' % name)

        # silently drop unknown options as long as they are not duplicates
        if convertor is None:
            dropped.add(name)
            continue

        # continue as before
        try:
            options[name] = convertor(value)
        except (ValueError, TypeError) as detail:
            raise detail.__class__('(option: "%s"; value: %r)\n%s'
                                   % (name, value, ' '.join(detail.args)))
    return options


utils.extract_extension_options = extract_extension_options


class ReadMeHTMLTranslator(HTMLTranslator):

    # Overrides base class not to output `<object>` tag for SVG images.
    object_image_types = {}

    def emptytag(self, node, tagname, suffix="\n", **attributes):
        """Override this to add back the width/height attributes."""
        if tagname == "img":
            if "width" in node:
                attributes["width"] = node["width"]
            if "height" in node:
                attributes["height"] = node["height"]

        return super(ReadMeHTMLTranslator, self).emptytag(
            node, tagname, suffix, **attributes
        )


SETTINGS = {
    # Cloaking email addresses provides a small amount of additional
    # privacy protection for email addresses inside of a chunk of ReST.
    "cloak_email_addresses": True,

    # Prevent a lone top level heading from being promoted to document
    # title, and thus second level headings from being promoted to top
    # level.
    "doctitle_xform": True,

    # Prevent a lone subsection heading from being promoted to section
    # title, and thus second level headings from being promoted to top
    # level.
    "sectsubtitle_xform": True,

    # Set our initial header level
    "initial_header_level": 2,

    # Prevent local files from being included into the rendered output.
    # This is a security concern because people can insert files
    # that are part of the system, such as /etc/passwd.
    "file_insertion_enabled": False,

    # Halt rendering and throw an exception if there was any errors or
    # warnings from docutils.
    "halt_level": 2,

    # Output math blocks as LaTeX that can be interpreted by MathJax for
    # a prettier display of Math formulas.
    "math_output": "MathJax",

    # Disable raw html as enabling it is a security risk, we do not want
    # people to be able to include any old HTML in the final output.
    "raw_enabled": False,

    # Disable all system messages from being reported.
    "report_level": 5,

    # Use typographic quotes, and transform --, ---, and ... into their
    # typographic counterparts.
    "smart_quotes": True,

    # Strip all comments from the rendered output.
    "strip_comments": True,

    # Use the short form of syntax highlighting so that the generated
    # Pygments CSS can be used to style the output.
    "syntax_highlight": "short",
}


def render(raw, stream=None, **kwargs):
    if stream is None:
        # Use a io.StringIO as the warning stream to prevent warnings from
        # being printed to sys.stderr.
        stream = io.StringIO()

    settings = SETTINGS.copy()
    settings["warning_stream"] = stream

    writer = Writer()
    writer.translator_class = ReadMeHTMLTranslator

    try:
        parts = publish_parts(raw, writer=writer, settings_overrides=settings)
    except SystemMessage:
        rendered = None
    else:
        rendered = parts.get("docinfo", "") + parts.get("fragment", "")

    if rendered:
        return clean(rendered)
    else:
        return None
