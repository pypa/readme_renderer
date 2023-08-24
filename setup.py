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

import pathlib

import setuptools

base_dir = pathlib.Path(__file__).parent

with open(base_dir.joinpath("readme_renderer", "__about__.py")) as f:
    about = {}
    exec(f.read(), about)

with open(base_dir.joinpath("README.rst")) as f:
    long_description = f.read()


setuptools.setup(
    author=about["__author__"],
    long_description=long_description,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
)
