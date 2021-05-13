from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FlagsAppConfig(AppConfig):
    name = "app.flags"
    verbose_name = _("Flags")

    def ready(self):
        try:
            import app.flags.signals  # noqa F401
        except ImportError:
            pass
