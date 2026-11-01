import os
import pathlib
import subprocess
import sys
import tempfile
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


def non_utf8_environment():
    env = os.environ.copy()
    env.update(PYTHONUTF8="0", PYTHONCOERCECLOCALE="0", LC_ALL="C",
               PYTHONIOENCODING="utf-8")
    return env


@pytest.mark.parametrize("fmt", ["txt", "rst", "md"])
def test_cli_reads_utf8_with_non_utf8_locale(tmp_path, fmt):
    if fmt == "md":
        pytest.importorskip("comrak")
    source = "Unicode: \u4f60\u597d \U0001f40d"
    path = tmp_path / ("README." + fmt)
    path.write_text(source, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-X", "utf8=0", "-m", "readme_renderer", str(path)],
        env=non_utf8_environment(), capture_output=True, check=True,
    )
    assert source in result.stdout.decode("utf-8")


def test_cli_writes_utf8_with_non_utf8_locale(tmp_path):
    source = "Unicode: \u4f60\u597d \U0001f40d"
    output = tmp_path / "output.html"
    # Package metadata is already Unicode, so this isolates output encoding.
    code = (
        "from email.message import Message; "
        "import readme_renderer.__main__ as cli; "
        "message = Message(); "
        "message['Description-Content-Type'] = 'text/plain'; "
        f"message.set_payload({source!a}); "
        "cli.metadata = lambda _: message; "
        "cli.main()"
    )
    subprocess.run(
        [sys.executable, "-X", "utf8=0", "-c", code,
         "--package", "unicode-package", "--output", str(output)],
        env=non_utf8_environment(), capture_output=True, check=True,
    )
    assert source in output.read_text(encoding="utf-8")
