from django.contrib.auth import get_user_model

from auto_datatables.mixins import AjaxMixin
from auto_datatables.views import BaseDataTable

User = get_user_model()
fields = [
    "id",
    "first_name",
    "last_name",
    "username",
    "email",
    "is_active",
    "is_staff",
    "is_superuser",
]


class AjaxTableView(AjaxMixin, BaseDataTable):
    model = User
    fields = fields
    row_template_name = "user_card.html"
    paging = False
    search_fields = ["first_name", "last_name", "username", "email"]
    # fields = ["name", "about", "status", "date_joined", ]
    # fixedHeader = True
    dom = "Bfrtip"
