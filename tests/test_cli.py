import pathlib
import pytest
from readme_renderer.__main__ import main
import tempfile
from unittest import mock


@pytest.fixture(params=["test_CommonMark_001.md", "test_rst_003.rst",
                        "test_GFM_001.md", "test_txt_001.txt"])
def input_file(request):
    path = pathlib.Path("tests/fixtures", request.param)
    # Skip markdown tests if the cmarkgfm optional dependency is not installed.
    if path.suffix == ".md":
        pytest.importorskip("cmarkgfm")
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


def test_cli_explicit_format(input_file):
    fmt = input_file.suffix.lstrip(".")
    with input_file.open() as fp, \
            mock.patch("pathlib.Path.open", return_value=fp), \
            mock.patch("builtins.print") as print_:
        main(["-f", fmt, "no-file.invalid"])
        print_.assert_called_once()
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
