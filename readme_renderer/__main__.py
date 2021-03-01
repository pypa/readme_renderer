from __future__ import absolute_import, print_function
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Renders a .rst or .md README to HTML",
    )
    parser.add_argument("input", help="Input README file", type=argparse.FileType("r"))
    parser.add_argument(
        "-o",
        "--output",
        help="Output file (default: stdout)",
        type=argparse.FileType("w"),
        default="-",
    )
    args = parser.parse_args()

    if args.input.name.split(".")[-1].lower() == "md":
        # Delay import in case user has not installed with the [md] extra
        from readme_renderer.markdown import render
    elif args.input.name.split(".")[-1].lower() == "txt":
        from readme_renderer.txt import render
    else:
        # Default is rst to preserve backwards compatibility.
        from readme_renderer.rst import render

    rendered = render(args.input.read(), stream=sys.stderr)
    if rendered is None:
        sys.exit(1)
    print(rendered, file=args.output)
