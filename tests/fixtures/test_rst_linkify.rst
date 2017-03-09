multigtfs: GTFS as a Django app
===============================

.. image:: https://travis-ci.org/tulsawebdevs/django-multi-gtfs.svg?branch=master
    :target: https://travis-ci.org/tulsawebdevs/django-multi-gtfs

.. image:: https://coveralls.io/repos/github/tulsawebdevs/django-multi-gtfs/badge.svg?branch=django19
    :target: https://coveralls.io/github/tulsawebdevs/django-multi-gtfs

.. Omit badges from docs

**multigtfs** is an `Apache 2.0`_-licensed Django app that supports importing
and exporting of GTFS feeds.  All features of the `June 20, 2012 reference`_
are supported, including `all changes`_ up to February 17, 2014.
It allows multiple feeds to be stored in the database at once.

It requires a spatial databases compatible with GeoDjango_.  PostgreSQL_ 9.x
and PostGIS_ 2.x are recommended for development and production, since these
support all the GeoDjango features.

Status
------
multigtfs is ready for your GTFS project.

Point releases (0.4.1 to 0.4.2) should be safe, only adding features or fixing
bugs.  Minor updates (0.3.3 to 0.4.0) may include significant changes that will
break relying code.  In the worst case scenario, you may need to export your
GTFS feeds in the original version, update multigtfs and your code, and
re-import.

multigtfs works with Django 1.5 through 1.9. In the next version, support
will be limited to Django's supported releases, so if you are using an old
version you will want to update to at least 1.8, the long-term support (LTS)
release.

All valid GTFS feeds are supported for import and export.  This includes
feeds with extra columns not yet included in the GTFS spec, and feeds that
omit ``calendar.txt`` in favor of ``calendar_dates.txt`` (such as the TriMet
archive feeds).  If you find a feed that doesn't work, `file a bug`_!

See the `issues list`_ for more details on bugs and feature requests.

Example project
---------------
Check out the `example project <examples/explore/README.md>`_.

Development
-----------

:Code:           https://github.com/tulsawebdevs/django-multi-gtfs
:Issues:         https://github.com/tulsawebdevs/django-multi-gtfs/issues
:Dev Docs:       http://multigtfs.readthedocs.org/
:IRC:            irc://irc.freenode.net/tulsawebdevs


.. _`Apache 2.0`: http://choosealicense.com/licenses/apache/
.. _`June 20, 2012 reference`: https://developers.google.com/transit/gtfs/reference
.. _`all changes`: https://developers.google.com/transit/gtfs/changes#RevisionHistory
.. _PostgreSQL: http://www.postgresql.org
.. _PostGIS: http://postgis.refractions.net
.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _`file a bug`: https://github.com/tulsawebdevs/django-multi-gtfs/issues
.. _`issues list`: https://github.com/tulsawebdevs/django-multi-gtfs/issues?state=open
