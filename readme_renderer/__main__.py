import argparse
import pathlib
import sys
from email.message import Message
from importlib.metadata import metadata

from readme_renderer.markdown import render as render_md
from readme_renderer.rst import render as render_rst
from readme_renderer.txt import render as render_txt


def main(cli_args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Renders a .md, .rst, or .txt README to HTML",
    )
    parser.add_argument("-p", "--package", help="Get README from package metadata",
                        action="store_true")
    parser.add_argument("-f", "--format", choices=["md", "rst", "txt"],
                        help="README format (inferred from input file name or package)")
    parser.add_argument('input', help="Input README file or package name")
    parser.add_argument('-o', '--output', help="Output file (default: stdout)",
                        default='-')
    args = parser.parse_args(cli_args)

    content_format = args.format
    markdown_variant = "GFM"
    if args.package:
        message = metadata(args.input)
        source = message.get_payload()  # type: ignore[attr-defined] # noqa: E501,RUF100 https://peps.python.org/pep-0566/

        # Parse the media type when inferring the format, or when an explicit
        # Markdown format still needs its declared variant.
        if not content_format or content_format == "md":
            raw_content_type = message.get("Description-Content-Type", "text/x-rst")
            content_type = raw_content_type.split(";", 1)[0].strip().casefold()
            parsed_content_type = Message()
            parsed_content_type["Content-Type"] = raw_content_type

            if content_type in {"text/plain", "text/x-rst", "text/markdown"}:
                parameters = parsed_content_type.get_params() or []
                charsets = [
                    value for name, value in parameters[1:]
                    if name.casefold() == "charset"
                ]
                if len(charsets) > 1 or any(
                    not isinstance(charset, str) or charset.casefold() != "utf-8"
                    for charset in charsets
                ):
                    raise ValueError(
                        f"invalid content type {raw_content_type} for package "
                        "`long_description`"
                    )

            if content_type == "text/markdown":
                variant = parsed_content_type.get_param("variant")
                if variant == "CommonMark":
                    markdown_variant = "CommonMark"

        # Infer the format of the description from package metadata.
        if not content_format:
            if content_type == "text/x-rst":
                content_format = "rst"
            elif content_type == "text/markdown":
                content_format = "md"
            elif content_type == "text/plain":
                content_format = "txt"
            else:
                raise ValueError(f"invalid content type {raw_content_type} for package "
                                 "`long_description`")
    else:
        filename = pathlib.Path(args.input)
        content_format = content_format or filename.suffix.lstrip(".")
        with filename.open() as fp:
            source = fp.read()

    if content_format == "md":
        rendered = render_md(source, variant=markdown_variant, stream=sys.stderr)
    elif content_format == "rst":
        rendered = render_rst(source, stream=sys.stderr)
    elif content_format == "txt":
        rendered = render_txt(source, stream=sys.stderr)
    else:
        raise ValueError(f"invalid README format: {content_format} (expected `md`, "
                         "`rst`, or `txt`)")
    if rendered is None:
        sys.exit(1)
    if args.output == "-":
        print(rendered, file=sys.stdout)
    else:
        with open(args.output, "w") as fp:
            print(rendered, file=fp)


if __name__ == '__main__':
    main()
