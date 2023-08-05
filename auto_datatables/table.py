import pprint

from django.core.exceptions import FieldDoesNotExist
from django.template.loader import get_template, render_to_string
from django.urls import resolve, reverse
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from drf_auto_endpoint.app_settings import settings
from rest_framework.utils import encoders, json

from .utils import template_to_js_literal


def serialize(obj):
    return json.dumps(obj, cls=encoders.JSONEncoder)


class DataTable:
    model = None
    config_class = None
    url = None
    table_id = ""

    # field declarations
    fields = []
    ordering_fields = []
    search_fields = []
    visible_fields = []
    hidden_fields = []
    extra_field_attributes = {}
    layout_overrides = {}

    # templating
    row_template = ""
    extra_row_template_context = {}

    # date formats - leave as None to let Luxon.js format dates based on locale
    date_format = None
    datetime_format = None
    time_format = None

    # misc
    debug = False
    DOM_ELEMENTS_MAP = {
        "l": ".dataTables_length",
        "f": ".dataTables_filter",
        "i": ".dataTables_info",
        "p": ".dataTables_paginate",
        "r": ".dataTables_processing",
        "t": ".dataTables_wrapper",
        "B": ".dt-buttons",
        # "R",
        # "S": ".dtsp-panes",
        "P": ".dtsp-panes",
        "Q": ".dtsb-searchBuilder",
    }

    def __init__(self, request=None, **kwargs):
        self.request = request
        self.model = kwargs.get("model", self.model)
        if self.model is None:
            raise ValueError("You must specify a model on the table or a queryset on the class.")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_id(self):
        """Returns the table id. If not specified, returns the class name."""
        return self.table_id or self.__class__.__name__

    def get_config(self):
        config = {}
        config["row_template"] = self.get_row_template()
        config["datatables"] = self.get_datatable_config()
        config["debug"] = self.debug
        config["metadata"] = self.get_metadata()
        config["layout"] = self.get_layout_config()
        config["widget_templates"] = self.get_widget_templates()
        config["field_templates"] = self.get_field_templates()
        config["datetime_format"] = self.datetime_format
        config["date_format"] = self.date_format
        config["time_format"] = self.time_format
        return config

    def get_js_config(self):
        return mark_safe(serialize(self.get_config()))  # noqa: S308

    def get_row_object(self):
        """Assigns each of the endpoint's fields the string "${FIELD_NAME}" so that each django template variable will be replaced with the equivalent js string literal tag.

        Doesn't work with nested fields.
        """
        base = {f: f"${{{ f }}}" for f in self.get_fields()}
        base.update(self.extra_row_template_context)
        return base

    def get_row_template(self):
        """Converts a django template to a js template literal by replacing django template tags with js template literal tags that contain field names from the endpoint."""
        row_obj = self.get_row_object()
        context = {
            "object": row_obj,
            self.model.__name__.lower(): row_obj,
        }
        if self.row_template:
            template = get_template(self.row_template)
            # pprint.pprint(dir(template.template))
            # pprint.pprint(template.template.render(Context()))
            return render_to_string(self.row_template, context=context, request=self.request)
        return ""

    def build_columns(self):
        """Build the columns for the datatable."""
        columns = []
        for field in self.get_fields():
            columns.append(self.build_column(field))
        return columns

    def build_column(self, field):
        """Build a column object for a single field."""
        try:
            verbose_name = getattr(self.model._meta.get_field(field), "verbose_name", None)
        except FieldDoesNotExist:
            verbose_name = None

        data = {
            "data": field,
            "name": field,
            "title": verbose_name or field.title(),
            "orderable": serialize(field in self.get_ordering_fields()),
            "searchable": serialize(field in self.search_fields),
            "visible": serialize(field in self.get_visible_fields()),
        }
        data.update(self.extra_field_attributes.get(field, {}))
        return data

    def get_ordering_fields(self):
        """Return the ordering fields for the datatable."""
        if getattr(self.config_class, "ordering", False) is True:
            return self.get_fields()
        return self.ordering_fields

    def get_fields(self):
        """Return the fields for the datatable."""
        if self.serializer_class:
            return [key for key in self.serializer_class().get_fields().keys()]
        return self.fields

    def get_visible_fields(self):
        """Return the fields for the datatable."""
        if len(self.visible_fields) > 0 and len(self.hidden_fields) > 0:
            raise ValueError("You cannot specify both visible_fields and hidden_fields.")
        if self.visible_fields:
            return self.visible_fields
        if self.hidden_fields:
            return [f for f in self.get_fields() if f not in self.hidden_fields]
        return self.get_fields()

    def get_datatable_config(self):
        obj = self.config_class
        return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("__")}

    def get_layout_config(self):
        """Return the layout for the datatable."""
        config = {}
        for k, v in self.layout_overrides.items():
            if k in self.DOM_ELEMENTS_MAP:
                config[self.DOM_ELEMENTS_MAP[k]] = v
            else:
                config[k] = v
        return config

    def get_widget_templates(self):
        """Return the field render templates for the datatable."""
        widget_mapping = getattr(settings, "WIDGET_MAPPING", {})
        # widget_mapping.update({"ImageField": "image"})
        templates = {}
        for widget_type in set(widget_mapping.values()):
            template = getattr(self, f"{widget_type}_widget_template", None)
            if template:
                templates[widget_type] = template_to_js_literal(template_str=template)

        return templates

    def get_field_templates(self):
        """Return the field render templates for the datatable."""
        templates = {}
        for field in self.get_fields():
            template = getattr(self, f"{field}_template", None)
            if template:
                templates[field] = template_to_js_literal(template_str=template)

        return templates

    def get_metadata(self):
        """Return the metadata for the datatable."""
        if self.url:
            view = import_string(resolve(self.url)._func_path)
            return view().options(request=self.request).data
        return {}
