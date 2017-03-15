"""Register models in Admin Panel."""

from django.contrib import admin
from snabb.app_info.models import AppInfo

admin.site.register(AppInfo)
