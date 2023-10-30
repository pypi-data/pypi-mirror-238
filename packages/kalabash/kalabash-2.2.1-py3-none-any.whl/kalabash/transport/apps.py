from django.apps import AppConfig


class TransportConfig(AppConfig):
    name = "kalabash.transport"

    def ready(self):
        from . import handlers  # NOQA:F401
