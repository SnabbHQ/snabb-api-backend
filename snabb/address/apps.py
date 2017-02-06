from django.apps import AppConfig


class AddressConfig(AppConfig):
    name = 'snabb.address'
    verbose_name = "Addresses"

    def ready(self):
        pass
