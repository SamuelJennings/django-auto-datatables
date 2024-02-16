from django.contrib.auth import get_user_model

from auto_datatables.views import DataTableBaseView

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
    "date_joined",
]


# searchPanes = {
#     # "threshold": 0.5,
#     "cascadePanes": True,
#     "orderable": False,
#     "controls": True,
#     "viewCount": False,
#     # "viewTotal": True,
#     "dtOpts": {
#         "searching": True,
#         "pagingType": "numbers",
#         "paging": True,
#     },
# }


class SimpleAjaxTable:
    deferRender = True
    ordering = True
    paging = True
    fixedHeader = True
    # dom = "PBfrtip"
    page_size = 100
    scrollX = True
    scrollY = 400


class ServerSideProcessing(SimpleAjaxTable):
    serverSide = True
    page_size = 25
    paging = True


class BaseTable(DataTableBaseView):
    model = User
    fields = fields
    search_fields = [
        "last_name",
    ]
    hidden_fields = ["id"]

    # email_template = "<a href='mailto:{{object.data}}'>{{object.data}}</a>"
    email_template = '<a href="mailto:${data}"><i class="fa-solid fa-envelope"></i></a>'
    # text_widget_template = "<h1>{{object.data}}</h1>"
    first_name_template = "<span class='text-primary'>{{object.data}}</span>"


class AjaxTable(BaseTable):
    # row_template_name = "user_card.html"
    table_config_class = SimpleAjaxTable
    debug = True


class ServerSideTable(BaseTable):
    table_config_class = ServerSideProcessing
    # row_template_name = "user_card.html"


class ScrollerConfig:
    serverSide = True
    scrollY = 300
    scroller = True
    deferRender = True
    ordering = True
    scrollX = True


class ScrollerTable(BaseTable):
    table_config_class = ScrollerConfig
    debug = True
