from json import JSONEncoder

from django.urls import include, path
from django.views.generic import TemplateView
from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import EndpointRouter
from rest_framework.fields import empty
from rest_framework.serializers import HyperlinkedModelSerializer

# from .router import CustomRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables import filters, pagination, renderers

from .mixins import ServerSideMixin

to_json = JSONEncoder().encode
from django.core.exceptions import FieldDoesNotExist


class BaseViewSet(ModelViewSet):
    renderer_classes = [renderers.DatatablesRenderer]
    filter_backends = [filters.DatatablesFilterBackend]


class BaseDataTable(Endpoint):
    view_class = TemplateView
    template_name = "auto_datatables/datatable.html"
    row_template_name: str = ""
    router_class = EndpointRouter
    base_viewset = BaseViewSet
    include_str = False
    pagination_class = pagination.DatatablesPageNumberPagination
    read_only = True
    # these are specific to this class
    hidden_fields = ["id"]
    extra_attributes = {}
    app_name: str = ""
    # defaults provided to datatables.net config
    rowId = "id"

    def __init__(self, name=None, **kwargs):
        self.name = name
        super().__init__(**kwargs)
        self.router = self.router_class()
        self.router.include_root_view = False

    def get_view(self):
        """Return a standard Django view that will be used to display the datatable."""
        return self.view_class.as_view(
            template_name=self.template_name,
            extra_context={"endpoint": self, "datatable_config": self.get_datatable_config()},
        )

    def get_name(self):
        """Return the name of the datatable."""
        return getattr(self, "name", None) or self.__class__.__name__

    def get_api_endpoint(self):
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

    def get_datatable_config(self):
        """Return the configuration for the datatable."""
        allowed_config = [
            "serverSide",
            "stateSave",
            "scrollY",
            "fixedHeader",
            "deferRender",
            "scroller",
            "rowId",
            "dom",
            "paging",
        ]
        return {val: getattr(self, val) for val in allowed_config if hasattr(self, val)}

    def get_datatables_columns(self):
        """Build the columns for the datatable."""
        columns = []
        for field in self.get_fields_from_serializer():
            columns.append(self.get_datatables_column(field))
        return columns

    def get_datatables_column(self, field):
        """Build a single column for the datatable."""
        data = self.extra_attributes.get(field, {})
        try:
            f = self.model._meta.get_field(field)
        except FieldDoesNotExist:
            data.update(data=field, name=field, title=field.title())
        else:
            data.update(
                data=field,
                name=field,
                title=f.verbose_name,
                orderable=to_json(field in self.get_ordering_fields()),
                searchable=to_json(field in self.get_search_fields()),
                visible=to_json(field not in self.get_hidden_fields()),
            )
        # print(data)
        return data

    def register(self, **kwargs):
        """Register the datatable with the router."""
        self.router.register(endpoint=self, **kwargs)

    @classmethod
    def as_view(cls, name=None, **initkwargs):
        self = cls(name=name, **initkwargs)
        self.register(**initkwargs)
        return include((self.router.urls, self.get_name()))


class BaseDataTable(Endpoint):
    view_class = TemplateView
    template_name = "auto_datatables/datatable.html"
    row_template_name: str = ""
    router_class = EndpointRouter
    base_viewset = BaseViewSet
    include_str = False
    pagination_class = pagination.DatatablesPageNumberPagination
    read_only = True
    # these are specific to this class
    hidden_fields = ["id"]
    extra_attributes = {}
    app_name: str = ""
    # defaults provided to datatables.net config
    rowId = "id"

    def __init__(self, name=None, **kwargs):
        self.name = name
        super().__init__(**kwargs)
        self.router = self.router_class()
        self.router.include_root_view = False

    def before_register(self):
        pass

    def after_register(self):
        pass

    def get_view(self):
        """Return a standard Django view that will be used to display the datatable."""
        return self.view_class.as_view(
            template_name=self.template_name,
            extra_context={"endpoint": self, "datatable_config": self.get_datatable_config()},
        )

    def get_name(self):
        """Return the name of the datatable."""
        return getattr(self, "name", None) or self.__class__.__name__

    def get_api_endpoint(self):
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

    def get_datatable_config(self):
        """Return the configuration for the datatable."""
        allowed_config = [
            "serverSide",
            "stateSave",
            "scrollY",
            "fixedHeader",
            "deferRender",
            "scroller",
            "rowId",
            "dom",
            "paging",
        ]
        return {val: getattr(self, val) for val in allowed_config if hasattr(self, val)}

    def get_datatables_columns(self):
        """Build the columns for the datatable."""
        columns = []
        for field in self.get_fields_from_serializer():
            columns.append(self.get_datatables_column(field))
        return columns

    def get_datatables_column(self, field):
        """Build a single column for the datatable."""
        data = self.extra_attributes.get(field, {})
        try:
            f = self.model._meta.get_field(field)
        except FieldDoesNotExist:
            data.update(data=field, name=field, title=field.title())
        else:
            data.update(
                data=field,
                name=field,
                title=f.verbose_name,
                orderable=to_json(field in self.get_ordering_fields()),
                searchable=to_json(field in self.get_search_fields()),
                visible=to_json(field not in self.get_hidden_fields()),
            )
        # print(data)
        return data

    def register(self, **kwargs):
        """Register the datatable with the router."""
        self.before_register()
        self.router.register(endpoint=self, **kwargs)
        self.after_register()

    @classmethod
    def as_view(cls, name=None, **initkwargs):
        self = cls(name=name, **initkwargs)
        self.register(**initkwargs)
        urls = [
            path("", self.get_view(), name="view"),
            path("", include(self.router.urls)),
        ]

        return include((urls, self.get_name()))


class ServerSideTable(ServerSideMixin, BaseDataTable):
    pass
