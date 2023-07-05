class AjaxMixin:
    deferRender = True
    pagination_class = None
    # page_size = None


class ServerSideMixin:
    serverSide = True
    deferRender = True


class ScrollerMixin(ServerSideMixin):
    page_size = 100
    scrollY = "100vh"
    scroller = True


class EditorMixin:
    read_only = False
