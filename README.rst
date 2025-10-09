Readme Renderer
===============

.. image:: https://badge.fury.io/py/readme-renderer.svg
    :target: https://badge.fury.io/py/readme-renderer

.. image:: https://github.com/pypa/readme_renderer/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/pypa/readme_renderer/actions/workflows/ci.yml

Readme Renderer is a library that will safely render arbitrary
``README`` files into HTML. It is designed to be used in Warehouse_ to
render the ``long_description`` for packages. It can handle Markdown,
reStructuredText (``.rst``), and plain text.

.. _Warehouse: https://github.com/pypa/warehouse


Check Description Locally
-------------------------

To locally check whether your long descriptions will render on PyPI, first
build your distributions, and then use the |twine check|_ command.


Code of Conduct
---------------

Everyone interacting in the readme_renderer project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the `PSF Code of Conduct`_.


Contributing
------------
Contributions are welcome, and they are greatly appreciated!
Every little bit helps. See `CONTRIBUTING.md`_ file for more information.


.. |twine check| replace:: ``twine check``
.. _twine check: https://packaging.python.org/guides/making-a-pypi-friendly-readme#validating-restructuredtext-markup
.. _PSF Code of Conduct: https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md
.. _CONTRIBUTING.md: https://github.com/pypa/readme_renderer/blob/main/.github/CONTRIBUTING.md

Copyright © 2014, [The Python Packaging Authority].
