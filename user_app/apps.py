from django.apps import AppConfig


class UserAppConfig(AppConfig):
    name = 'user_app'
    
    def ready(self):
        from .api.signals import create_auth_token, save_user_profile, create_user_profile
