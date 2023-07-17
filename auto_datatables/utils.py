# import TextChoices from django
import re

from django.db.models import Choices
from django.template import loader

styles = [
    {
        "datatables": "dt",
        "bootstrap3": "bs3",
        "bootstrap4": "bs4",
        "bootstrap5": "bs5",
        "bulma": "bm",
        "foundation": "zf",
        "jqueryui": "ju",
        "fomantic": "se",
    },
]


def template_to_js_literal(template_name="", template_str=""):
    """Converts a django template to a js template literal"""
    if not template_name and not template_str:
        raise ValueError("Either template_name or template_str must be provided")
    if not template_str:
        # get the template string
        template_str = loader.get_template(template_name).template.source

    # matches django template tags
    pattern = r"{{\s*([\w.]+)\s*}}"

    # in order to modify the match, we need to define a function to pass to re.sub
    def modify_match(match):
        """Replace django template tags with js template literal tags"""
        return "${" + ".".join(match.group(1).split(".")[1:]) + "}"

    return re.sub(pattern, modify_match, template_str)
