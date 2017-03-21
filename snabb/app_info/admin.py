"""Register models in Admin Panel."""

from django.contrib import admin
from snabb.app_info.models import AppInfo


class AppInfoAdmin(admin.ModelAdmin):

    model = AppInfo
    list_display = ['name', 'updated_at', 'active']


admin.site.register(AppInfo, AppInfoAdmin)
