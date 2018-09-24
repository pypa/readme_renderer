Readme Renderer
===============

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
chat rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.


.. |twine check| replace:: ``twine check``
.. _twine check: https://packaging.python.org/guides/making-a-pypi-friendly-readme#validating-restructuredtext-markup
.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
