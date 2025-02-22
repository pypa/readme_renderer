#!/usr/bin/env bash
set -e

# `tox` testing manages its own environments
# Create virtualenv for local development, editor completion, etc.
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[md]
