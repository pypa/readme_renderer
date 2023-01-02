import pathlib
import pytest
from readme_renderer.__main__ import __main__
import tempfile
from unittest import mock


@pytest.mark.parametrize("input_file", ["test_CommonMark_001.md", "test_rst_003.rst"])
@pytest.mark.parametrize("output_file", [False, True])
def test_cli_input_file(input_file, output_file):
    input_file = pathlib.Path("tests/fixtures", input_file)

    if output_file:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = pathlib.Path(tmpdir) / "output.html"
            __main__(["-o", str(output), str(input_file)])
            with output.open() as fp:
                result = fp.read()
    else:
        with mock.patch("builtins.print") as print_:
            __main__([str(input_file)])
            print_.assert_called_once()
            (result,), _ = print_.call_args

    with input_file.with_suffix(".html").open() as fp:
        expected = fp.read()
    assert result.strip() == expected.strip()


@pytest.mark.parametrize("package, contains", [
    ("readme_renderer", "Readme Renderer is a library that will safely render"),
    ("docutils", "Docutils is a modular system for processing documentation"),
])
def test_cli_package(package, contains):
    with mock.patch("builtins.print") as print_:
        __main__(["-p", package])
        print_.assert_called_once()
        (result,), _ = print_.call_args
    assert contains in result
