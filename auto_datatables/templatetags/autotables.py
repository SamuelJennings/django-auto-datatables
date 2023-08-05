from django import template

register = template.Library()


@register.inclusion_tag("auto_datatables/table.html", takes_context=True)
def render_table(context):
    return context


@register.inclusion_tag("auto_datatables/render_for_url.html", takes_context=True)
def render_table_for_url(context, table, fetch_metadata=False):
    context["table"] = table
    return context
