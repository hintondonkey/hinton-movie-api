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
    if created and instance:
        broker = None
        current_user = User.objects.filter(id=instance.current_user_id).first()
        account_type = AccountType.objects.filter(name=instance.account_type).first()
        if account_type == AccountTypeEnum.BUSINESS_ADMIN.value or instance.is_superuser:
            broker = Broker.objects.create(name=instance.username, is_network=instance.is_superuser)
        else:
            broker = Broker.objects.filter(id=current_user.profile.broker_id if current_user and current_user.profile else None).first()
        
        profile = Profile.objects.create(user=instance, account_type=account_type, broker=broker)
        if not profile.broker:
            is_super_admin = False
            if account_type == AccountTypeEnum.BUSINESS_ADMIN.value or instance.is_superuser:
                is_super_admin = True
            Profile.objects.filter(id=profile.id).update(broker=broker, is_super_admin=is_super_admin)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()