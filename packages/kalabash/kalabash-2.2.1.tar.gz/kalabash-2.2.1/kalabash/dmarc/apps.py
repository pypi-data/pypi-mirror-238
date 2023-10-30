"""AppConfig for dmarc."""

from django.apps import AppConfig

from kalabash.dmarc.forms import load_settings


class DmarcConfig(AppConfig):
    """App configuration."""

    name = "kalabash.dmarc"
    verbose_name = "Kalabash DMARC tools"

    def ready(self):
        load_settings()
        from . import handlers
