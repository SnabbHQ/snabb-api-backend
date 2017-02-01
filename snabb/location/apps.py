from django.apps import AppConfig


class LocationConfig(AppConfig):
    name = 'snabb.location'
    verbose_name = "Locations"

    def ready(self):
        pass
