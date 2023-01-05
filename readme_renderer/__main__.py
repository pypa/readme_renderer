import argparse
import email
from readme_renderer.markdown import render as render_md
from readme_renderer.rst import render as render_rst
from readme_renderer.txt import render as render_txt
import pathlib
from pkg_resources import get_distribution
import sys


def __main__(args=None):  # noqa: N807
    parser = argparse.ArgumentParser(
        description="Renders a .md, .rst, or .txt README to HTML",
    )
    parser.add_argument("-p", "--package", help="Get README from package metadata",
                        action="store_true")
    parser.add_argument("-f", "--format", choices=["md", "rst", "txt"],
                        help="README format (inferred from input file name or package)")
    parser.add_argument('input', help="Input README file or package name")
    parser.add_argument('-o', '--output', help="Output file (default: stdout)",
                        type=argparse.FileType('w'), default='-')
    args = parser.parse_args(args)

    content_format = args.format
    if args.package:
        distribution = get_distribution(args.input)
        pkg_info = distribution.get_metadata(distribution.PKG_INFO)
        message = email.message_from_string(pkg_info)
        source = message.get_payload()

        # Infer the format of the description from package metadata.
        if not content_format:
            content_type = message.get("Description-Content-Type", "text/x-rst")
            if content_type == "text/x-rst":
                content_format = "rst"
            elif content_type == "text/markdown":
                content_format = "md"
            elif content_type == "text/plain":
                content_format = "txt"
            else:
                raise ValueError(f"invalid content type {content_type} for package "
                                 "`long_description`")
    else:
        filename = pathlib.Path(args.input)
        content_format = content_format or filename.suffix.lstrip(".")
        with filename.open() as fp:
            source = fp.read()

    if content_format == "md":
        render = render_md
    elif content_format == "rst":
        render = render_rst
    elif content_format == "txt":
        render = render_txt
    else:
        raise ValueError(f"invalid README format: {content_format} (expected `md`, "
                         "`rst`, or `txt`)")
    rendered = render(source, stream=sys.stderr)
    if rendered is None:
        sys.exit(1)
    print(rendered, file=args.output)


if __name__ == '__main__':
    __main__()
