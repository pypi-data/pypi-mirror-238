import django
from django.apps import AppConfig

if django.get_version() > '4.0':
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _


class DateRangeFilterAppConfig(AppConfig):
    name = 'daterangefilter'
    verbose_name = _('Date Range Filter')
