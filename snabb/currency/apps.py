from django.apps import AppConfig


class CurrencyConfig(AppConfig):
    name = 'snabb.currency'
    verbose_name = "Currencies"

    def ready(self):
        pass
