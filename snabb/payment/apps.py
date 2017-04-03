from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'snabb.payment'
    verbose_name = 'Payment'

    def ready(self):
        pass
