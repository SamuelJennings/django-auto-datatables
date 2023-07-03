# Django Laboratory 

[![Github Build](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-auto-datatables/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-auto-datatables)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-auto-datatables)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-auto-datatables)
![PyPI](https://img.shields.io/pypi/v/django-auto-datatables)
<!-- [![RTD](https://readthedocs.org/projects/django-auto-datatables/badge/?version=latest)](https://django-auto-datatables.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/build-docs.yml/badge.svg)](https://github.com/SSJenny90/django-auto-datatables/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/SSJenny90/django-auto-datatables)](https://github.com/SSJenny90/django-auto-datatables/pulls)
[![Issues](https://img.shields.io/github/issues-raw/SSJenny90/django-auto-datatables)](https://github.com/SSJenny90/django-auto-datatables/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-auto-datatables) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/django-auto-datatables) -->

A scientific auto-datatables management app for Django

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-auto-datatables/

Quickstart
----------

Install Django Laboratory::

    pip install django-auto-datatables

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'auto-datatables',
        ...
    )

Add Django Laboratory's URL patterns:

    urlpatterns = [
        ...
        path('', include("auto-datatables.urls")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

