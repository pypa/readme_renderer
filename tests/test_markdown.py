import io
import os
import textwrap

from readme.markdown import render


def test_simple():
    markdown_markup = 'Hello'
    out, rendered = render(markdown_markup)
    assert rendered
    assert out == '<p>Hello</p>'


def test_url_no_link():
    markdown_markup = 'http://mymalicioussite.com/'
    out, rendered = render(markdown_markup)
    expected_html = '<p>http://mymalicioussite.com/</p>'
    assert rendered
    assert out == expected_html


def test_iframe():
    markdown_markup = """\
        <iframe src="http://mymalicioussite.com/">Click here</iframe>
    """.strip()
    out, rendered = render(markdown_markup)
    expected_html = ''.join([
        '&lt;iframe src="http://mymalicioussite.com/"&gt;'
        'Click here&lt;/iframe&gt;'])
    assert rendered
    assert out == expected_html


def test_script():
    markdown_markup = textwrap.dedent("""\
        <script>
            alert("Hello");
        </script>""")
    out, rendered = render(markdown_markup)
    expected_html = textwrap.dedent("""\
        &lt;script&gt;
            alert("Hello");
        &lt;/script&gt;""")
    assert rendered
    assert out == expected_html


def test_a_tag_gets_nofollow():
    markdown_markup = '<a href="http://mymalicioussite.com/">Click here</a>'
    out, rendered = render(markdown_markup)
    expected_htmls = [
        ''.join(['<p><a rel="nofollow" href="http://mymalicioussite.com/">',
                 'Click here</a></p>']),
        ''.join(['<p><a href="http://mymalicioussite.com/" rel="nofollow">',
                 'Click here</a></p>']),
    ]
    assert rendered
    assert out in expected_htmls


def test_headings_and_paragraphs():
    _do_test_with_files('headings_and_paragraphs')


def test_misc():
    _do_test_with_files('misc')


def _do_test_with_files(test_name, expected_rendered=True):
    md_markup = read('{0}.md'.format(test_name))
    expected_html = read('{0}.html'.format(test_name))

    out, rendered = render(md_markup)

    assert rendered == expected_rendered
    assert out == expected_html.rstrip()


def read(fn):
    path = os.path.join(os.path.dirname(__file__), 'fixtures', 'markdown', fn)
    with io.open(path, encoding='utf-8') as f:
        return f.read()
