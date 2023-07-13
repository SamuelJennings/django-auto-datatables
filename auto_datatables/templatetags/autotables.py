from django import template

# from django.conf import settings
from django.templatetags.static import static
from quantityfield import settings

register = template.Library()


@register.inclusion_tag("auto_datatables/table.html", takes_context=True)
def render_table(context):
    return context
