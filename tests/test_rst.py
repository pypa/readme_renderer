import codecs
import os

from readme.rst import render


def test_rst_001():
    assert render('Hello') == ('<p>Hello</p>\n', True)


def test_rst_002():
    assert render('http://mymalicioussite.com/') == (
        ('<p><a href="http://mymalicioussite.com/" rel="nofollow">' +
         'http://mymalicioussite.com/</a></p>\n'),
        True)


def test_rst_003():
    _do_test_with_files('test_rst_003')


def test_rst_004():
    _do_test_with_files('test_rst_004')


def test_rst_005():
    _do_test_with_files('test_rst_005')


def test_rst_006():
    _do_test_with_files('test_rst_006')


def test_rst_007():
    _do_test_with_files('test_rst_007', expected_rendered=False)


def test_rst_008():
    _do_test_with_files('test_rst_008')


def _do_test_with_files(test_name, expected_rendered=True):
    rst_markup = read('{0}.rst'.format(test_name))
    expected_html = read('{0}.html'.format(test_name))

    out, rendered = render(rst_markup)

    assert rendered == expected_rendered
    assert out == expected_html


def read(fn):
    path = os.path.join(os.path.dirname(__file__), 'fixtures', fn)
    with codecs.open(path, encoding='utf-8') as f:
        return f.read()
