from django.apps import AppConfig


class QuoteConfig(AppConfig):
    name = 'snabb.quote'
    verbose_name = "Quotes"

    def ready(self):
        pass
