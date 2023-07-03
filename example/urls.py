from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import AjaxTableView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("simple-ajax/", AjaxTableView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
