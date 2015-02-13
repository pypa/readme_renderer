readme
======

Readme is a library that will safely render arbitrary README files into HTML.
It is designed to be used in Warehouse_ to render the ``long_description`` for packages.

.. _Warehouse: https://github.com/pypa/warehouse


Check Description Locally
-------------------------

To check your long description's locally simply install the readme library
using:

.. code-block:: console

    $ pip install readme
    $ python setup.py check -r -s
