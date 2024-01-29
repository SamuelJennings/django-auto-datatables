import pprint

from django.shortcuts import render
from django.views.generic.base import ContextMixin
from django_filters.rest_framework import DjangoFilterBackend
from drf_auto_endpoint.factories import serializer_factory
from drf_auto_endpoint.metadata import AutoMetadata
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_datatables.pagination import DatatablesPageNumberPagination

from .filters import SearchPanesFilter
from .renderers import DatatablesRenderer
from .table import DataTable


class AutoTableMixin(ContextMixin):
    table = DataTable
    table_overrides = {}
    template_name = "auto_datatables/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = self.table(request=self.request, **self.table_overrides)
        context["template"] = self.table.row_template
        return context


class DataTableBaseView(ListAPIView, AutoTableMixin):
    renderer_classes = [TemplateHTMLRenderer, DatatablesRenderer]
    filter_backends = [DjangoFilterBackend, SearchPanesFilter]
    metadata_class = AutoMetadata
    base_serializer_class = None
    filter_by_user = False

    def get(self, request, *args, **kwargs):
        if self.request.accepted_renderer.format == "html":
            return render(request, self.template_name, context=self.get_context_data())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        if not getattr(self.table, "model", None):
            raise ValueError("You must specify a model on the table or a queryset on the class.")
        return self.table.model.objects.all()

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        return serializer_factory(model=self.table.model, fields=self.fields, base_class=self.base_serializer_class)

    @property
    def paginator(self):
        """If serverside processing is enabled, return the datatables paginator, otherwise return None."""
        DT_CONFIG = self.table.config_class
        if not hasattr(self, "_paginator"):
            if not getattr(DT_CONFIG, "serverSide", None):
                self._paginator = None
            else:
                self._paginator = DatatablesPageNumberPagination()
        return self._paginator
