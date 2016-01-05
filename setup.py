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

import os
import textwrap
import setuptools
import warnings

base_dir = os.path.dirname(__file__)

warnings.warn(textwrap.dedent("""
    The "readme" library was renamed to "readme_renderer"
    to work around an installation issue that could prevent
    it from being installed on some systems.

    Please install the "readme_renderer" library instead:
    https://pypi.python.org/pypi/readme_renderer"""))


with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


setuptools.setup(
    name='readme',
    version='0.7.1',

    description=('readme is a library for rendering "readme" descriptions for '
                 'Warehouse'),
    long_description=long_description,
    license='Apache License, Version 2.0',
    url='https://github.com/pypa/readme',

    author='Donald Stufft',
    author_email='donald@stufft.io',

    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],

    py_modules=['wheel-platform-tag-is-broken-on-empty-wheels-see-issue-141'],
    install_requires=['readme_renderer']
)
