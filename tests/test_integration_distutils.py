import distutils.dist
import unittest.mock

import pytest
import setuptools.dist

import readme_renderer.integration.distutils


def test_valid_rst():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description="Hello, I am some text."))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_not_called()


def test_invalid_rst():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description="Hello, I am some `totally borked< text."))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()
    checker.announce = unittest.mock.Mock()

    checker.check_restructuredtext()

    # Should warn once for the syntax error, and finally to warn that the
    # overall syntax is invalid
    checker.warn.assert_called_once_with(unittest.mock.ANY)
    message = checker.warn.call_args[0][0]
    assert 'invalid markup' in message
    assert 'line 1: Warning:' in message
    assert 'start-string without end-string' in message

    # Should not have announced that it was valid.
    checker.announce.assert_not_called()


def test_malicious_rst():
    description = """
.. raw:: html
    <script>I am evil</script>
"""
    dist = distutils.dist.Distribution(attrs=dict(
        long_description=description))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()
    checker.announce = unittest.mock.Mock()

    checker.check_restructuredtext()

    # Should warn once for the syntax error, and finally to warn that the
    # overall syntax is invalid
    checker.warn.assert_called_once_with(unittest.mock.ANY)
    message = checker.warn.call_args[0][0]
    assert 'directive disabled' in message

    # Should not have announced that it was valid.
    checker.announce.assert_not_called()


@pytest.mark.filterwarnings('ignore:::distutils.dist')
def test_markdown():
    dist = setuptools.dist.Distribution(attrs=dict(
        long_description="Hello, I am some text.",
        long_description_content_type="text/markdown"))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_called()
    assert 'content type' in checker.warn.call_args[0][0]


def test_invalid_missing():
    dist = distutils.dist.Distribution(attrs=dict())
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_called_once_with(unittest.mock.ANY)
    assert 'missing' in checker.warn.call_args[0][0]


def test_invalid_empty():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description=""))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = unittest.mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_called_once_with(unittest.mock.ANY)
    assert 'missing' in checker.warn.call_args[0][0]
