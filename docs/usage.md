# Usage


## Table Options

Django Auto Datatables provides a number of options for configuring your tables. These options are passed to the table constructor as keyword arguments.

- row_template_name = ""
- table_config_class = None
- fields = []
- extra_field_attributes = {}
- layout_overrides: dict = {}
- extra_row_template_context = {}
- ordering_fields = []
- search_fields = []
- hidden_fields = []

**optional attributes**

These attributes are optional and define template that will be used to render the cell contents for a given field or widget type. To specify a template for a widget, use the following syntax:

{{widget_type}}_widget_template = "<p> a template {{ data }} </p"

This will apply the template to all fields that use the specified widget type.

To specify a template for a single field, use:

{{field_name}}_template = "<p> a template {{ data }} </p"

Note: Field templates take precedence over widget templates.


## Simple AJAX Tables

Simple AJAX Tables are the most basic type in Django Auto Datatables. If you have a relatively small amount of data that you wish to display asynchronously, this is the type for you. No pagination is provided on the serverside so the entire dataset is downloaded each time the table is initialized.



## Serverside Processing




## Scroller




## Field Type Templating

Django Auto Datatables provides a simple way to employ field templating in Datatables.net tables. 

For any widget type defined in settings.DRF_AUTO_WIDGET_MAPPING, you can specify a display template on your model by setting the attribute `{WIDGET_TYPE}_template` and passing a valid templating string. 

Available default widgets provided by DRF Auto Endpoint are:

- `checkbox`
- `null-boolean`
- `number`
- `foreignkey`
- `tomany-table`
- `textarea`
- `select`
- `date`
- `time`
- `datetime`
- `text`
- `email`
- `url`
- `manytomany-lists`
- `generic-foreignkey`
- `duration`

To provide a template for an email field and a null-boolean field, you would configure your table as follows: 

```python

class MyModel(models.Model):
    email_template = 'mailto:{{ data }}'
    null_boolean_template = '{% if data %}Yes{% else %}No{% endif %}'

```

## Row Templating




## DOM Placement