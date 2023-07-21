# Django Auto Datatables 

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

Django Auto Datatables is a high-level API for creating datatables(.net) in Django. It provides a simple API for creating interactive datatables with minimal effort. The package supports all the features of datatables.net and allows for easy customization of the datatable. It also supports server-side processing and the scroller plugin for large API driven datatables.

## Documentation

The full documentation is at https://ssjenny90.github.io/django-auto-datatables/

## Table of Contents

- [Django Auto Datatables](#django-auto-datatables)
  - [Documentation](#documentation)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Views](#views)
  - [Templates](#templates)
  - [Template Tags](#template-tags)
  - [Settings](#settings)
  - [Contributing](#contributing)
  - [License](#license)
  - [Changelog](#changelog)
  - [Support and Contact](#support-and-contact)
  - [Features](#features)
  - [Experimental Features](#experimental-features)
  - [Running Tests](#running-tests)
  - [Development commands](#development-commands)
  - [Acknowledgments](#acknowledgments)





## Usage

Usage examples and guides on how to use your package in a Django project.

## Configuration

Configuration options and settings available in your package.


## Views

AutoTableMixin:




## Templates

This package provides a single template which is called if the `render_table` template tag is used without arguments. The template is located at `auto_datatables/table.html` and can be overridden by creating a template with the same name in your project.

## Template Tags

Django Auto Datatables provides the following template tags:

- `render_table`: This tag can be used to render a datatable in a template. The tag accepts the current context and expects a number of variables to be present. Make sure to subclass any view with the BaseViewMixin to ensure the correct variables are present in the context.

## Settings

AUTO_DATATABLES_DEFAULT_RENDERER = 'auto_datatables.renderers.DatatablesRenderer'

- The default renderer to use when rendering the datatable. Defaults to 'auto_datatables.renderers.DatatablesRenderer'.


## Contributing

Contributor guidelines can be found in the [How to Contribute](CONTRIBUTING.md) file.

## License

This project is provided under the [MIT License](LICENSE).

## Changelog

[Change Log](CHANGELOG.md) is a log of changes made to the package. It is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## Support and Contact

A section to provide information about where users can get support for your package and how they can contact you for inquiries or issues.




## Features

- Simple API for creating interactive datatables
- Allows for easy customization of the datatable
- Supports all the features of datatables.net
- Supports server-side processing

## Experimental Features

- Templated row output

## Running Tests

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


## Development commands

    pip install -r requirements_dev.txt
    invoke -l

## Acknowledgments

Django Auto Datatables relies heavily on previous work by the following projects:

- [Django Rest Framework Datatables](https://github.com/izimobil/django-rest-framework-datatables)
- [DRF Schema Adapter](https://github.com/drf-forms/drf-schema-adapter)



