from django.dispatch import receiver
from django.db.models.signals import post_save
from ..models import *
from hintonmovie.globals import AccountTypeEnum


@receiver(post_save, sender=User) 
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        account_type = AccountType.objects.filter(name=instance.account_type).first()
        current_user = User.objects.filter(id=instance.current_user_id).first()
        broker = None
        if account_type == AccountTypeEnum.BUSINESS_ADMIN.value:
            broker = Broker.objects.create(name=instance.username)
        
        Profile.objects.create(user=instance, account_type=account_type, broker=broker)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()