from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = 'services'
    
    def ready(self):
        from .api.signals import create_broker_service