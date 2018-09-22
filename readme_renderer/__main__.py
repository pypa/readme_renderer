from __future__ import absolute_import, print_function
from readme_renderer.rst import render
import sys


if len(sys.argv) == 2:
    with open(sys.argv[1]) as fp:
        out = render(fp.read(), stream=sys.stderr)
        if out is not None:
            print(out)
        else:
            sys.exit(1)
else:
    print("Syntax: python -m readme_renderer <file.rst>", file=sys.stderr)
