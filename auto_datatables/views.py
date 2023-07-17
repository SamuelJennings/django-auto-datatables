from json import JSONEncoder

from django.core import serializers
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from rest_framework.utils import encoders, json

from .utils import template_to_js_literal


class DataTableBaseView(TemplateView):
    template_name = "auto_datatables/base.html"
    row_template = ""
    endpoint = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endpoint"] = self.endpoint
        context["config"] = self.get_config()
        context["templated"] = self.get_row_template()
        return context

    def get_config(self):
        config = {}
        config["row_template"] = self.get_row_template()
        config["metadata"] = self.get_metadata()
        config["datetime_format"] = self.endpoint.datetime_format
        config["date_format"] = self.endpoint.date_format
        config["time_format"] = self.endpoint.time_format
        config["email_template"] = self.endpoint.email_template
        config["link_template"] = self.endpoint.link_template
        config["image_template"] = self.endpoint.image_template
        config["boolean_templates"] = self.endpoint.boolean_templates
        return mark_safe(json.dumps(config, cls=encoders.JSONEncoder))

    def get_metadata(self):
        """Returns the metadata for the endpoint."""
        return self.endpoint.viewset().options(request=self.request).data

    def pre_filter_queryset(self, queryset):
        return queryset

    def get_row_template_context(self):
        """Assigns each of the endpoint's fields the string "${FIELD_NAME}" so that each django template variable will be replaced with the equivalent js string literal tag."""
        return {f: f"${{{ f }}}" for f in self.endpoint.fields}

    def get_row_template(self):
        """Converts a django template to a js template literal by replacing django template tags with js template literal tags that contain field names from the endpoint."""
        template = self.endpoint.row_template_name or self.row_template
        model_name = self.endpoint.model.__name__.lower()
        context = {
            "object": self.get_row_template_context(),
            model_name: self.get_row_template_context(),
        }
        if template:
            return render_to_string(template, context=context, request=self.request)
        return None
