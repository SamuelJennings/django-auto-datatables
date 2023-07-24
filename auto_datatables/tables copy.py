from json import JSONEncoder

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.urls import include, path
from django_filters.rest_framework import DjangoFilterBackend
from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.metadata import AutoMetadata
from drf_auto_endpoint.router import EndpointRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables import pagination

from .filters import AutoSearchPanesFilter
from .renderers import DatatablesRenderer
from .utils import template_to_js_literal
from .views import DataTableBaseView

to_json = JSONEncoder().encode


class BaseViewSet(ModelViewSet):
    renderer_classes = [DatatablesRenderer]
    filter_backends = [DjangoFilterBackend, AutoSearchPanesFilter]
    metadata_class = AutoMetadata


class TableEndpoint(Endpoint):
    view_class = DataTableBaseView
    base_viewset = BaseViewSet
    pagination_class = pagination.DatatablesPageNumberPagination
    include_str = False
    read_only = True
    # router_class = EndpointRouter
    # base_serializer = serializers.ModelSerializer


class BaseDataTable(TableEndpoint):
    """Base class for all datatables."""

    table_config_class = None

    class DTConfig:
        serverSide = True
        stateSave = True
        scrollY = "50vh"
        fixedHeader = True
        deferRender = True
        scroller = True
        pageLength = 25
        paging = True
        dom = "lfrtip"
        searchPanes = True

    # these are specific to this class
    template_name = ""
    app_name: str = ""
    row_template_name = ""
    orderable = True
    extra_row_template_context = {}
    field_render_templates = {}
    hidden_fields = ["id"]
    search_panes = []
    extra_attributes = {}
    layout: dict = {}
    # email_template = '<a href="mailto:{{data}}">{{data}}</a>'
    # link_template = '<a href="{{data}}">{{data}}</a>'
    # image_template = '<img src="{{data}}">'
    boolean_templates = {
        "true": '<i class="fas fa-check">{{data}}</i>',
        "false": '<i class="fas fa-times">{{data}}</i>',
        "null": '<i class="fas fa-minus">{{data}}</i>',
    }
    date_format = "YYYY-MM-DD"
    datetime_format = "YYYY-MM-DD HH:mm:ss"
    time_format = "HH:mm:ss"
    # defaults provided to datatables.net config
    rowId = "pk"

    DOM_MAP = {
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

    def __init__(self, name=None, **kwargs):
        self.name = name
        super().__init__(**kwargs)
        self.router = EndpointRouter()
        self.router.include_root_view = False
        # self.router = self.router_class()

    def get_field_render_templates(self):
        """Return the field render templates for the datatable."""
        widget_mapping = getattr(settings, "DRF_AUTO_WIDGET_MAPPING", {})

        widget_templates = {}
        for widget_type in widget_mapping.values():
            template = getattr(self, f"{widget_type}_template", None)
            if template:
                widget_templates[widget_type] = template_to_js_literal(template_str=template)

        return widget_templates

    def get_search_panes(self):
        """Return the search panes for the datatable."""
        return self.search_panes

    def get_layout(self):
        """Return the layout for the datatable."""
        config = {}
        for k, v in self.layout.items():
            if k in self.DOM_MAP:
                config[self.DOM_MAP[k]] = v
            else:
                config[k] = v
        return config

    def get_context_data(self, **kwargs):
        """Context data that will be given to the underlying view class."""
        return {}

    def get_view(self):
        """Return a standard Django view that will be used to display the datatable."""
        return self.view_class.as_view(
            endpoint=self,
            extra_context=self.get_context_data(),
        )

    def get_name(self):
        """Return the name of the datatable."""
        return getattr(self, "name", None) or self.__class__.__name__

    def get_api_endpoint(self):
        """Returns a string that can be reversed to get the API endpoint for the datatable."""
        endpoint = f"{self.get_name()}:{self.model._meta.object_name.lower()}-list"
        if self.app_name:
            endpoint = f"{self.app_name}:{endpoint}"
        return endpoint

    def get_hidden_fields(self):
        """Return a list of fields that should be hidden from the datatable."""
        return self.hidden_fields or []

    def get_url(self):
        """Return the URL for the datatable."""
        return self.model._meta.object_name.lower()

    def get_fields_from_serializer(self):
        """Return the fields from the serializer."""
        return self.serializer().fields.keys()

    # def get_datatable_config(self):
    #     """Return the configuration for the datatable."""
    #     allowed_config = [
    #         "serverSide",
    #         "stateSave",
    #         "scrollY",
    #         "fixedHeader",
    #         "deferRender",
    #         "scroller",
    #         "rowId",
    #         "dom",
    #         "paging",
    #         "searchPanes",
    #         "pageLength",
    #     ]
    #     return {val: getattr(self, val) for val in allowed_config if hasattr(self, val)}

    def get_datatable_config(self):
        return {k: v for k, v in vars(self.DTConfig).items() if not k.startswith("__")}

    def get_datatables_columns(self):
        """Build the columns for the datatable."""
        columns = []
        for field in self.get_fields_from_serializer():
            columns.append(self.get_column_props(field))
        return columns

    def get_column_props(self, field):
        """Gets the column properties for a single field."""
        try:
            verbose_name = self.model._meta.get_field(field).verbose_name
        except FieldDoesNotExist:
            verbose_name = None

        data = {
            "data": field,
            "name": field,
            "title": verbose_name or field.title(),
            "orderable": to_json(field in self.get_ordering_fields() or self.orderable),
            "searchable": to_json(field in self.get_search_fields()),
            "visible": to_json(field not in self.get_hidden_fields()),
        }
        data.update(self.get_extra_attributes(field))
        return data

    def get_extra_attributes(self, field):
        """Return extra attributes for a field."""
        return self.extra_attributes.get(field, {})

    @classmethod
    def as_view(cls, name=None, **initkwargs):
        self = cls(name=name, **initkwargs)
        self.router.register(endpoint=self, **initkwargs)
        urls = [
            path("", self.get_view(), name="view"),
            path("", include(self.router.urls)),
        ]

        return include((urls, self.get_name()))
