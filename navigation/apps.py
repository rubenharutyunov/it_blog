from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NavigationConfig(AppConfig):
    name = 'navigation'
    verbose_name = _("Navigation")
