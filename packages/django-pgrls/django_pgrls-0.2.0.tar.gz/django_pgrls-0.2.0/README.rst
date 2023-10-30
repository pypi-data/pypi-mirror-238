
django-pgrls
============

.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg
      :alt: Packaging: Poetry
      :target: https://python-poetry.org/

.. image:: https://github.com/lorinkoz/django-pgrls/workflows/code/badge.svg
      :alt: Build status
      :target: https://github.com/lorinkoz/django-pgrls/actions

.. image:: https://readthedocs.org/projects/django-pgrls/badge/?version=latest
      :alt: Documentation status
      :target: https://django-pgrls.readthedocs.io/

.. image:: https://coveralls.io/repos/github/lorinkoz/django-pgrls/badge.svg?branch=master
      :alt: Code coverage
      :target: https://coveralls.io/github/lorinkoz/django-pgrls?branch=master

.. image:: https://badge.fury.io/py/django-pgrls.svg
      :alt: PyPi version
      :target: https://badge.fury.io/py/django-pgrls

.. image:: https://pepy.tech/badge/django-pgrls/month
      :alt: Downloads
      :target: https://pepy.tech/project/django-pgrls

|

This app uses Postgres row level security to support data multi-tenancy in a
single Django project. `Row level security`_ allows automatic row filtering on
the database side.

.. _Row level security: https://www.postgresql.org/docs/current/ddl-rowsecurity.html

Documentation
-------------

https://django-pgrls.readthedocs.io/

Contributing
------------

- Join the discussion at https://github.com/lorinkoz/django-pgrls/discussions.
- PRs are welcome! If you have questions or comments, please use the discussions
  link above.
- To run the test suite run ``make``. The tests for this project live inside a
  small django project called ``sandbox``.
