import distutils.dist

import mock

import readme_renderer.integration.distutils


def test_valid_rst():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description="Hello, I am some text."))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_not_called()


def test_invalid_rst():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description="Hello, I am some `totally borked< text."))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = mock.Mock()

    checker.check_restructuredtext()

    # Should warn once for the syntax error, and finally to warn that the
    # overall syntax is invalid
    checker.warn.call_count = 2
    message_one = checker.warn.call_args_list[0][0][0]
    assert 'start-string without end-string' in message_one
    message_two = checker.warn.call_args_list[1][0][0]
    assert 'invalid markup' in message_two


def test_invalid_missing():
    dist = distutils.dist.Distribution(attrs=dict())
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_called_once_with(mock.ANY)
    assert 'missing' in checker.warn.call_args[0][0]


def test_invalid_empty():
    dist = distutils.dist.Distribution(attrs=dict(
        long_description=""))
    checker = readme_renderer.integration.distutils.Check(dist)
    checker.warn = mock.Mock()

    checker.check_restructuredtext()

    checker.warn.assert_called_once_with(mock.ANY)
    assert 'missing' in checker.warn.call_args[0][0]
