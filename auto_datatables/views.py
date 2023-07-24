from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from drf_auto_endpoint.app_settings import settings
from drf_auto_endpoint.factories import serializer_factory
from drf_auto_endpoint.metadata import AutoMetadata
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.utils import encoders, json
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination

from .filters import SearchPanesFilter
from .renderers import DatatablesRenderer
from .utils import template_to_js_literal


def serialize(obj):
    return json.dumps(obj, cls=encoders.JSONEncoder)


class DataTableBaseView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, DatatablesRenderer]
    # filter_backends = [SearchPanesFilter, DatatablesFilterBackend]
    filter_backends = [DjangoFilterBackend, SearchPanesFilter]
    metadata_class = AutoMetadata
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
    debug = False
    filter_by_user = False
    template_name = "auto_datatables/base.html"
    row_template_name = ""
    table_config_class = None
    fields = []
    extra_field_attributes = {}
    layout_overrides: dict = {}
    extra_row_template_context = {}
    ordering_fields = []
    search_fields = []
    hidden_fields = []
    date_format = ""
    datetime_format = ""
    time_format = ""
    base_serializer_class = None

    def get(self, request, *args, **kwargs):
        if self.request.accepted_renderer.format == "html":
            return render(request, self.template_name, context=self.get_context_data())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.filter_by_user:
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.all()

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        return serializer_factory(
            model=self.model, fields=self.fields, base_class=self.base_serializer_class
        )

    def get_context_data(self, **kwargs):
        context = {}
        context["config"] = self.get_config()
        context["view"] = self
        context["templated"] = len(self.get_row_template()) > 0
        return context

    def get_config(self):
        config = {}
        config["row_template"] = self.get_row_template()
        config["metadata"] = self.options(self.request).data
        config["datatables"] = self.get_datatable_config()
        config["debug"] = self.debug
        config["layout"] = self.get_layout_config()
        config["widget_templates"] = self.get_widget_templates()
        config["field_templates"] = self.get_field_templates()
        config["datetime_format"] = self.datetime_format
        config["date_format"] = self.date_format
        config["time_format"] = self.time_format

        return mark_safe(serialize(config))  # noqa: S308

    def get_row_object(self):
        """Assigns each of the endpoint's fields the string "${FIELD_NAME}" so that each django template variable will be replaced with the equivalent js string literal tag.

        Doesn't work with nested fields.
        """
        base = {f: f"${{{ f }}}" for f in self.fields}
        base.update(self.extra_row_template_context)
        return base

    def get_row_template(self):
        """Converts a django template to a js template literal by replacing django template tags with js template literal tags that contain field names from the endpoint."""
        row_obj = self.get_row_object()
        context = {
            "object": row_obj,
            self.model.__name__.lower(): row_obj,
        }
        if self.row_template_name:
            return render_to_string(
                self.row_template_name, context=context, request=self.request
            )
        return ""

    def build_columns(self):
        """Build the columns for the datatable."""
        columns = []
        for field in self.fields:
            columns.append(self.build_column(field))
        return columns

    def build_column(self, field):
        """Build a column object for a single field."""
        try:
            verbose_name = self.model._meta.get_field(field).verbose_name
        except FieldDoesNotExist:
            verbose_name = None

        data = {
            "data": field,
            "name": field,
            "title": verbose_name or field.title(),
            "orderable": serialize(field in self.get_ordering_fields()),
            "searchable": serialize(field in self.search_fields),
            "visible": serialize(field not in self.hidden_fields),
        }
        data.update(self.extra_field_attributes.get(field, {}))
        return data

    def get_ordering_fields(self):
        """Return the ordering fields for the datatable."""
        if getattr(self.table_config_class, "ordering", False) is True:
            return self.fields
        return self.ordering_fields

    def get_datatable_config(self):
        return {
            k: v
            for k, v in vars(self.table_config_class).items()
            if not k.startswith("__")
        }

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
        for field in self.fields:
            template = getattr(self, f"{field}_template", None)
            if template:
                templates[field] = template_to_js_literal(template_str=template)

        return templates

    @property
    def paginator(self):
        """If serverside processing is enabled, return the datatables paginator, otherwise return None."""
        table = self.table_config_class
        if not hasattr(self, "_paginator"):
            if not getattr(table, "serverSide", None):
                self._paginator = None
            else:
                self._paginator = DatatablesPageNumberPagination()
        return self._paginator
