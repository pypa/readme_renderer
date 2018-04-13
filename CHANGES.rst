Changes
=======

20.0 (2018-04-13)
-----------------

* Reformat docutils messages into more human-friendly output. (#92)
* Fix incorrect escaping of html entities in pre tags when using markdown. (#89)
* Allow width, height, alt, and align attributes on img tags. (#91)
* Fix check to not report success when there is invalid RST. (#90)


19.0 (2018-04-10)
-----------------

* Allow details and summary tags. (#77)
* Add .pytest_cache to .gitignore. (#85)
* Warn about Markdown content type when checking RST. (#83)
* Update pep8 tox env to use py3.6. (#84)
* Add Pygments-based syntax highlighting for Markdown. (#82)
* Update docs about check to talk about Markdown. (#80)


18.1 (2018-04-01)
-----------------

* Change Github-flavored Markdown identifier from ``gfm`` to ``GFM``.


18.0 (2018-03-30)
-----------------

* Add support for GitHub-flavored Markdown. (#67)
* Switch to cmarkgfm completely for rendering Markdown. (#68)
* Warn about missing long description. (#69)
* Make Github-Flavored Markdown the default variant (#73)


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
