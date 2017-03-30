from django.apps import AppConfig


class DispatchingConfig(AppConfig):
    name = 'snabb.dispatching'
    verbose_name = "Dispatching"

    def ready(self):
        pass
