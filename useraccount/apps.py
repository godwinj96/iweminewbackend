from django.apps import AppConfig


class UseraccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useraccount'

    def ready(self):
        import useraccount.signals
        print("Signal handlers registered")
