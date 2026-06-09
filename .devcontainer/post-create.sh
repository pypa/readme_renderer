#!/usr/bin/env bash
set -e

# Local dev venv for IDE completion, running the package, etc.
# tox + tox-uv are pre-installed in the image.
uv venv --clear
# Mirror tox.ini's [testenv] deps so the IDE's Test Explorer and
# `Debug current pytest file` launch config can import pytest.
uv pip install -e ".[md]" pytest pytest-cov pytest-icdiff
