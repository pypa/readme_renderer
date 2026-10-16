import pathlib
import tempfile
from email.message import Message
from unittest import mock

import pytest

from readme_renderer.__main__ import main


@pytest.fixture(params=["test_CommonMark_001.md", "test_rst_003.rst",
                        "test_GFM_001.md", "test_txt_001.txt"])
def input_file(request):
    path = pathlib.Path("tests/fixtures", request.param)
    # Skip markdown tests if the comrak optional dependency is not installed.
    if path.suffix == ".md":
        pytest.importorskip("comrak")
    return path


@pytest.mark.parametrize("output_file", [False, True])
def test_cli_input_file(input_file, output_file):
    with mock.patch("builtins.print") as print_:
        if output_file:
            with tempfile.TemporaryDirectory() as tmpdir:
                output = pathlib.Path(tmpdir) / "output.html"
                main(["-o", str(output), str(input_file)])
                with output.open() as fp:
                    result = fp.read()
        else:
            main([str(input_file)])

    print_.assert_called_once()
    (result,), kwargs = print_.call_args

    with input_file.with_suffix(".html").open() as fp:
        expected = fp.read()
    assert result.strip() == expected.strip()

    if output_file:
        assert kwargs["file"].name == str(output)


def test_cli_invalid_format():
    with mock.patch("pathlib.Path.open"), \
            pytest.raises(ValueError, match="invalid README format: invalid"):
        main(["no-file.invalid"])


def test_cli_explicit_format(input_file, tmp_path):
    fmt = input_file.suffix.lstrip(".")

    temp_input = tmp_path / "invalid.invalid"
    temp_input.write_text(input_file.read_text())

    with mock.patch("builtins.print") as print_:
        main(["-f", fmt, str(temp_input)])
        (result,), _ = print_.call_args

    with input_file.with_suffix(".html").open() as fp:
        assert result.strip() == fp.read().strip()


@pytest.mark.parametrize("package, contains", [
    ("readme_renderer", "Readme Renderer is a library that will safely render"),
    ("docutils", "Docutils is a modular system for processing documentation"),
])
def test_cli_package(package, contains):
    with mock.patch("builtins.print") as print_:
        main(["-p", package])
        print_.assert_called_once()
        (result,), _ = print_.call_args
    assert contains in result


@pytest.mark.parametrize(("content_type", "source", "contains"), [
    ("text/x-rst; charset=UTF-8", "A paragraph.", "<p>A paragraph.</p>"),
    ("text/plain; charset=UTF-8", "A paragraph.", "A paragraph."),
])
def test_cli_package_parameterized_content_type(content_type, source, contains):
    message = Message()
    message["Description-Content-Type"] = content_type
    message.set_payload(source)

    with mock.patch("readme_renderer.__main__.metadata", return_value=message), \
            mock.patch("builtins.print") as print_:
        main(["--package", "fixture"])
        (result,), _ = print_.call_args

    assert contains in result


@pytest.mark.parametrize(("content_type", "contains", "explicit_format"), [
    ("text/markdown; charset=UTF-8; variant=GFM", "<del>strike</del>", False),
    ("TEXT/MARKDOWN; CHARSET=\"UTF-8\"; VARIANT=\"CommonMark\"", "~~strike~~", False),
    ("text/markdown; charset=UTF-8; variant=CommonMark", "~~strike~~", True),
    ("text/markdown; charset=UTF-8; variant=Unsupported", "<del>strike</del>", False),
    ("text/markdown; charset=UTF-8; variant=commonmark", "<del>strike</del>", False),
])
def test_cli_package_markdown_variant(content_type, contains, explicit_format):
    pytest.importorskip("comrak")
    message = Message()
    message["Description-Content-Type"] = content_type
    message.set_payload("~~strike~~")
    cli_args = ["--package", "fixture"]
    if explicit_format:
        cli_args.extend(["--format", "md"])

    with mock.patch("readme_renderer.__main__.metadata", return_value=message), \
            mock.patch("builtins.print") as print_:
        main(cli_args)
        (result,), _ = print_.call_args

    assert contains in result


@pytest.mark.parametrize("content_type", [
    "text/markdown; charset=ISO-8859-1",
    "not a media type",
])
def test_cli_package_rejects_invalid_content_type(content_type):
    message = Message()
    message["Description-Content-Type"] = content_type
    message.set_payload("README")

    with mock.patch("readme_renderer.__main__.metadata", return_value=message), \
            pytest.raises(ValueError, match="invalid content type"):
        main(["--package", "fixture"])
