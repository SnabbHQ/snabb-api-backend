from django.apps import AppConfig


class ContactConfig(AppConfig):
    name = 'snabb.contact'
    verbose_name = "Contacts"

    def ready(self):
        pass
