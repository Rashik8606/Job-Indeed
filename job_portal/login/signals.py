from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'  # Replace with your app name

    def ready(self):
        import login.signals  # Replace with your app name
