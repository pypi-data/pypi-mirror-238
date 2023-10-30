"""AppConfig for admin."""

from django.apps import AppConfig

from .app_settings import load_admin_settings


class AdminConfig(AppConfig):
    """App configuration."""

    name = "kalabash.admin"
    verbose_name = "Kalabash admin console"

    def ready(self):
        load_admin_settings()

        from . import handlers  # NOQA:F401
