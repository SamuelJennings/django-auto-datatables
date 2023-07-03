from json import JSONEncoder

from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView


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
