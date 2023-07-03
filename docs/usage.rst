=====
Usage
=====

To use Django Laboratory in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'auto-datatables.apps.LaboratoryConfig',
        ...
    )

Add Django Laboratory's URL patterns:

.. code-block:: python

    from auto-datatables import urls as auto-datatables_urls


    urlpatterns = [
        ...
        url(r'^', include(auto-datatables_urls)),
        ...
    ]
