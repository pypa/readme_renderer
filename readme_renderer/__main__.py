from __future__ import absolute_import, print_function
import argparse
from readme_renderer.rst import render
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Renders a .rst README to HTML",
    )
    parser.add_argument('input', help="Input README file")
    parser.add_argument('-o', '--output', help="Output file (default: stdout)")
    args = parser.parse_args()
    if args.output:
        output_file = open(args.output, 'w')
    else:
        output_file = sys.stdout
    input_file = open(args.input)

    rendered = render(input_file.read(), stream=sys.stderr)
    if rendered is None:
        sys.exit(1)
    print(rendered, file=output_file)
