from django.apps import AppConfig


class SizeConfig(AppConfig):
    name = 'snabb.size'
    verbose_name = "Sizes"

    def ready(self):
        pass
