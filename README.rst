Readme Renderer
================

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


Configure Rendering
-------------------

Markdown callers can pass ``comrak.ExtensionOptions`` and
``comrak.RenderOptions`` as keyword-only ``extension_options`` and
``render_options`` arguments::

    import comrak
    from readme_renderer.markdown import render

    extensions = comrak.ExtensionOptions()
    extensions.strikethrough = True
    html = render("~~removed~~", extension_options=extensions)

Each supplied object replaces that category of options. A fresh Comrak options
object has Comrak's defaults, not the renderer's GFM defaults. Omitted arguments
retain the selected variant's existing defaults. Caller objects and module
options are not modified, and the resulting HTML is still sanitized. Custom
``header_id_prefix`` values are also applied to relative heading links.

For reStructuredText, pass a ``settings_overrides`` mapping to override individual
Docutils settings for one call::

    from readme_renderer.rst import render

    html = render("Heading\n=======\n", settings_overrides={
        "initial_header_level": 3,
    })

Omitted settings retain their defaults. Enabling ``file_insertion_enabled`` or
``raw_enabled`` raises ``ValueError`` to preserve the renderer's safety
restrictions. The explicit ``stream`` argument takes precedence over a
``warning_stream`` setting. Treat rendering options as application configuration,
not as options supplied by untrusted documents.


Code of Conduct
---------------

Everyone interacting in the readme_renderer project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the `PSF Code of Conduct`_.


Contributing
------------
Contributions are welcome. See `CONTRIBUTING.md`_ for setup and testing.


.. |twine check| replace:: ``twine check``
.. _twine check: https://packaging.python.org/guides/making-a-pypi-friendly-readme#validating-restructuredtext-markup
.. _PSF Code of Conduct: https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md
.. _CONTRIBUTING.md: https://github.com/pypa/readme_renderer/blob/main/.github/CONTRIBUTING.md

Copyright © 2014, The Python Packaging Authority.
