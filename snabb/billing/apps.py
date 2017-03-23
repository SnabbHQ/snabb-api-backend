from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = 'snabb.billing'
    verbose_name = "Billing"

    def ready(self):
        pass
