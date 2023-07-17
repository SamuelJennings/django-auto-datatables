from json import JSONEncoder

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView

from .utils import template_to_js_literal


class DataTableBaseView(TemplateView):
    template_name = "auto_datatables/base.html"
    row_template = ""
    endpoint = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endpoint"] = self.endpoint
        # context["datatable_config"] = JSONEncoder().encode(self.endpoint.get_datatable_config())
        context["row_template"] = self.get_row_template()
        # context["endpoint_url"] = self.get_endpoint_url()
        return context

    def pre_filter_queryset(self, queryset):
        return queryset

    def get_row_template(self):
        template = self.endpoint.row_template_name or self.row_template
        if template:
            return template_to_js_literal(template)
        return None

    # def get_row_template_str(self):
    #     template = self.get_row_template()
    #     if template:
    #         return replace_placeholder(template.template.source)

    # def get_endpoint_url(self):
    #     if self.endpoint_name:
    #         return reverse(self.endpoint_name)
    #     return self.endpoint.get_url()


class DataTableViewMixin(TemplateView):
    endpoint = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endpoint"] = self.endpoint
        context["datatable_config"] = JSONEncoder().encode(self.endpoint.get_datatable_config())
        return context

    @classonlymethod
    def as_view(cls, endpoint=None, **initkwargs):
        endpoint = endpoint or cls.endpoint
        endpoint.register(**initkwargs)
        super().as_view(**initkwargs)


class DataTableView(DataTableViewMixin, TemplateView):
    pass
