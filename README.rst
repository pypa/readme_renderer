Readme Renderer
===============

Readme Renderer is a library that will safely render arbitrary
``README`` files into HTML. It is designed to be used in Warehouse_ to
render the ``long_description`` for packages. It can handle Markdown,
reStructuredText (``.rst``), and plain text.

.. _Warehouse: https://github.com/pypa/warehouse


Check Description Locally
-------------------------

reStructuredText
~~~~~~~~~~~~~~~~

To locally check whether your reStructuredText long descriptions will render on
PyPI, simply install the ``readme_renderer`` library using:

.. code-block:: console

    $ pip install readme_renderer
    $ python setup.py check -r -s
    running check

If there's a problem rendering your ``long_description``, the check
will tell you. If your ``long_description`` is fine, you'll get no
output.


Markdown
~~~~~~~~

Checking your Markdown long descriptions is unecessary, because unlike rST,
where a properly rendered description is all-or-nothing, PyPI will still render
your Markdown description as Markdown if it has some invalid or incorrect
syntax.


Render Markup Locally
---------------------

You can render the HTML that will be generated from your ``long_description`` using:

.. code-block:: console

	$ python setup.py render_readme

The rendered HTML will be output to the console by default.

If you would like to send the output to a web browser instead, use the ``--preview`` flag:

.. code-block:: console

	$ python setup.py render_readme --preview

You can also control the Pygments style used in syntax highlighting using the
``--style`` flag, or eliminate syntax highlighting altogether by using the
``--no-color`` flag:

.. code-block:: console

	$ python setup.py render_readme --style=monokai # <-- Pygments style name
	$ python setup.py render_readme --no-color


Code of Conduct
---------------

Everyone interacting in the readme_renderer project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
