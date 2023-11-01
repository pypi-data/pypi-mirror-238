from django.apps import AppConfig
from rhazes.context import ApplicationContext
from django.conf import settings


class DjangoBootCoreConfig(AppConfig):
    name = "django_boot_core"

    def ready(self):
        to_scan = ["django_boot_core.services"]
        if hasattr(settings, "DI_PACKAGES") and type(settings.DI_PACKAGES) == list:
            to_scan += settings.DI_PACKAGES
        ApplicationContext.initialize(to_scan)
