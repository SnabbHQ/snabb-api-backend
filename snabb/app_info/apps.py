from django.apps import AppConfig


class AppInfoConfig(AppConfig):
    name = 'snabb.app_info'
    verbose_name = "AppInfo"

    def ready(self):
        pass
