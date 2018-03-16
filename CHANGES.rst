Changes
=======

17.4 (2018-03-16)
-----------------

* All renderers now accept arbitrary ``kwargs`` for future-proofing.


17.3 (2018-03-08)
-----------------

* Gracefully handle new exceptions from bleach.


17.2 (2017-03-11)
-----------------

* Fix an issue cleaning plaintext values.


17.1 (2017-03-09)
-----------------

* Fix an issue attempting to clean data that had ``<a>`` tags without a href.


17.0 (2017-03-08)
-----------------

* Fix issue with bleach >= 2.0.


16.0 (2016-12-09)
-----------------

* Fix issue with docutils >= 0.13.1.


0.7.0 (2016-01-04)
------------------

* Renamed to ``readme_renderer``: https://github.com/pypa/readme_renderer
  to work around an name overlap with ``README`` files shipped in Python's
  default site-packages directory on certain case-insensitive file systems.

* Added `PyPA Code of Conduct`_.

* Allow <sub> and <sup> tags when cleaning rST HTML output.

* Dropped support for Python 2.6.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
