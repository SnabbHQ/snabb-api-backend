from django.apps import AppConfig


class CouriersConfig(AppConfig):
    name = 'snabb.couriers'
    verbose_name = "Couriers"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
