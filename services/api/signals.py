from django.dispatch import receiver
from django.db.models.signals import post_save
from ..models import *
from user_app.models import User, Broker
from hintonmovie.globals import *


@receiver(post_save, sender=Category)
def create_broker_service(sender, instance, created, **kwargs):
    if created and instance:
        try:
            broker_list = Broker.objects.all()

            for broker in broker_list:
                # business_admin = User.objects.filter()
                name = instance.name + ' Management'
                account_management = 'Account Management'
                if not BrokerService.objects.filter(name=name, broker=broker).exists():
                    BrokerService.objects.create(name=name, broker=broker, category=instance, price=10)
                if not BrokerService.objects.filter(name=account_management, broker=broker).exists():
                    BrokerService.objects.create(name=account_management, broker=broker, category=None, price=10)

        except Exception as e:
            print("Getting create_broker_service error as message: ", e)