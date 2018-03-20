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

import io
import webbrowser

from distutils.command.check import check as _check
from distutils.core import Command
from tempfile import NamedTemporaryFile

from ..rst import render


class Check(_check):
    def check_restructuredtext(self):
        """
        Checks if the long string fields are reST-compliant.
        """
        data = self.distribution.get_long_description()
        stream = io.StringIO()
        markup = render(data, stream=stream)

        for line in stream.getvalue().splitlines():
            if line.startswith("<string>"):
                line = line[8:]
            self.warn(line)

        if markup is None:
            self.warn("Invalid markup which will not be rendered on PyPI.")


class render_readme(Command):
    """Render and display the long description as HTML."""
    description = ("render the long description as HTML")
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Runs the command."""
        data = self.distribution.get_long_description()
        stream = io.StringIO()
        markup = render(data, stream=stream)

        for line in stream.getvalue().splitlines():
            if line.startswith("<string>"):
                line = line[8:]
            self.warn(line)

        if markup is None:
            self.warn("Invalid markup which will not be rendered on PyPI.")

        f = NamedTemporaryFile(
            prefix='render_readme_',
            suffix='.html',
            delete=False,
        )
        print('Writing readme to {0}'.format(f.name))
        f.write(markup.encode('utf-8'))

        webbrowser.open('file://' + f.name.replace('\\', '/'))
