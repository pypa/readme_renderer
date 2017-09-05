# Copyright 2017 Julien Palard
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

import mdorrst

from .rst import render as rst_renderer
from .markdown import render as md_renderer
from .txt import render as txt_renderer

RENDERERS = {'rst': rst_renderer,
             'md': md_renderer,
             'txt': txt_renderer}


def render(raw):
    sniffed_format = mdorrst.sniff(raw)
    return RENDERERS[sniffed_format](raw) or txt_renderer(raw)
