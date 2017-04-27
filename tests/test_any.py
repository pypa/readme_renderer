import io
import glob
import os.path

import pytest

from readme_renderer.any import render


@pytest.mark.parametrize(
    ("src_filename", "html_filename"),
    [
        (fn, os.path.splitext(fn)[0] + ".html")
        for fn in glob.glob(
            os.path.join(os.path.dirname(__file__),
                         "fixtures", "test_*.rst")
        ) + glob.glob(
            os.path.join(os.path.dirname(__file__),
                         "fixtures", "markdown", "*.md")
        )
    ],
)
def test_any_fixtures(src_filename, html_filename):
    too_short = {
        'misc.md',
        'test_rst_004.rst',
        'test_rst_005.rst',
        'test_rst_006.rst',
        'test_rst_007.rst'}
    if os.path.basename(src_filename) in too_short:
        """sniff won't match in any cases for those files being too short
        tests to be sniffed correctly (like just an "<a href", or just
        a <script>alert("Hello")</script>) """
        return
    # Get our Markup
    with io.open(src_filename, encoding='utf-8') as f:
        markup = f.read()

    # Get our expected
    with io.open(html_filename, encoding="utf-8") as f:
        expected = f.read()

    out = render(markup)

    assert out.rstrip() == expected.rstrip()
