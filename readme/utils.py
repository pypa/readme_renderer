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

import six


class Rendered(six.text_type):

    raw = None
    rendered = False

    @classmethod
    def from_rendered(cls, raw, rendered=None):
        # Use the rendered content and fallback to the raw content
        content = rendered if rendered is not None else raw

        # Create an instance of this type with the content
        obj = cls(content)

        # Store some details about the content
        obj.raw = raw
        obj.rendered = True if rendered is not None else False

        return obj
