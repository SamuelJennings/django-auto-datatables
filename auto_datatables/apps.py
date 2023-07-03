from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import gettext_lazy as _


class DataTablesConfig(AppConfig):
    name = "auto_datatables"
    label = "auto_datatables"
