import argparse
import email
from readme_renderer.rst import render
from pkg_resources import get_distribution
import sys


def __main__(args=None):
    parser = argparse.ArgumentParser(
        description="Renders a .rst README to HTML",
    )
    parser.add_argument("-p", "--package", help="Get README from package metadata",
                        action="store_true")
    parser.add_argument('input', help="Input README file or package name")
    parser.add_argument('-o', '--output', help="Output file (default: stdout)",
                        type=argparse.FileType('w'), default='-')
    args = parser.parse_args(args)

    if args.package:
        distribution = get_distribution(args.input)
        pkg_info = distribution.get_metadata(distribution.PKG_INFO)
        message = email.message_from_string(pkg_info)
        source = message.get_payload()
    else:
        with open(args.input) as fp:
            source = fp.read()
    rendered = render(source, stream=sys.stderr)
    if rendered is None:
        sys.exit(1)
    print(rendered, file=args.output)


if __name__ == '__main__':
    __main__()
