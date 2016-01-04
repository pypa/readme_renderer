readme
======

.. warning::

    The readme library was renamed to readme_renderer to work around an
    installation issue that could prevent it from being installed on
    some systems. Use the readme_renderer_ library instead.

Readme is a library that will safely render arbitrary README files into HTML.
It is designed to be used in Warehouse_ to render the ``long_description`` for packages.

.. _Warehouse: https://github.com/pypa/warehouse
.. _readme_renderer: https://pypi.python.org/pypi/readme_renderer

Check Description Locally
-------------------------

To check your long description's locally simply install the readme library
using:

.. code-block:: console

    $ pip install readme
    $ python setup.py check -r -s
