from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

# import TemplateView
from django.views.generic import TemplateView

from .views import AjaxTableView, ScrollerProcessing, ServerSideProcessing

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html")),
    path("admin/", admin.site.urls),
    path("ajax/", AjaxTableView.as_view()),
    path("server-side/", ServerSideProcessing.as_view()),
    path("scroller/", ScrollerProcessing.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
