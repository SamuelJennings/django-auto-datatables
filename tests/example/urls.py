from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

# import TemplateView
from django.views.generic import TemplateView

from .views import AjaxTable, ScrollerTable, ServerSideTable

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html")),
    path("admin/", admin.site.urls),
    path("simple-ajax/", AjaxTable.as_view(), name="simple-ajax"),
    path("server-side/", ServerSideTable.as_view(), name="server-side"),
    path("scroller/", ScrollerTable.as_view(), name="scroller"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
