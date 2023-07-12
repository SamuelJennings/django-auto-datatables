from django.contrib.auth import get_user_model

from auto_datatables.mixins import AjaxMixin, ScrollerMixin, ServerSideMixin
from auto_datatables.tables import BaseDataTable

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


class BaseTable(BaseDataTable):
    model = User
    fields = fields
    search_fields = ["first_name", "last_name", "username", "email"]
    searchPanes = {  # noqa: RUF012
        # "threshold": 0.5,
        "cascadePanes": True,
        "orderable": False,
        "controls": True,
        "viewCount": False,
        # "viewTotal": True,
        "dtOpts": {
            "searching": True,
            "pagingType": "numbers",
            "paging": True,
        },
    }


class AjaxTableView(AjaxMixin, BaseTable):
    # row_template_name = "user_card.html"
    paging = False
    fixedHeader = True
    dom = "PBfrtip"


class ServerSideProcessing(ServerSideMixin, BaseTable):
    dom = "Pfrtip"
    row_template_name = "user_card.html"

    # row_template_name = "user_card.html"


class ScrollerProcessing(ScrollerMixin, BaseTable):
    dom = "Pfrtip"
