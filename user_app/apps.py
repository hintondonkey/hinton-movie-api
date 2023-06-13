from django.apps import AppConfig


class UserAppConfig(AppConfig):
    name = 'user_app'
    
    def ready(self):
        from .api import signals
