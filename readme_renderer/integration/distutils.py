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

from distutils.command.check import check as _check

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
