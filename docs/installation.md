# Getting Started

## Installation

To install Django Auto Datatables, simply run:

    pip install django-auto-datatables

Add it to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...

        'auto_datatables',
        ...
    )

### Optional Dependencies

[DRF ORJSON Renderer](https://github.com/brianjbuck/drf_orjson_renderer) provides a huge speed boost over the DRF Json Serializer. If you are serializing large amounts of data and don't want to rely on serverside processing, you can install DRF ORJSON Renderer alongside Django Auto Datatables with following command:

    pip install django-auto-datatables[orjson]

## Installed 