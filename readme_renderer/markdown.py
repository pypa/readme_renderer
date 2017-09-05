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

import markdown

from .clean import clean


def render(raw):
    try:
        rendered = markdown.markdown(
            raw,
            extensions=[
                'markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.smart_strong',
            ])
    except ValueError:
        # Markdown failed to strip top-level tags.
        return None
    else:
        return clean(rendered)
