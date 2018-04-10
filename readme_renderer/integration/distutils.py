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

import distutils.log
from distutils.command.check import check as _check

from ..rst import render


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

        stream = io.StringIO()
        markup = render(data, stream=stream)

        for line in stream.getvalue().splitlines():
            if line.startswith("<string>"):
                line = line[8:]
            self.warn(line)

        if markup is None:
            self.warn(
                "The project's long_description has invalid markup which will "
                "not be rendered on PyPI.")

        self.announce(
            "The project's long description is valid RST.",
            level=distutils.log.INFO)
