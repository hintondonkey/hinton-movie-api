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
        try:
            broker = None
            account_type = None
            creating_user = User.objects.filter(id=instance.id).first()
            try:
                account_type = AccountType.objects.filter(name=instance.account_type).first()
            except Exception as e:
                print("Getting account_type_name error as message: ", e)

            if (account_type and account_type.name == AccountTypeEnum.BUSINESS_ADMIN.value) or creating_user.is_superuser:
                broker = Broker.objects.create(name=creating_user.username, is_network=creating_user.is_superuser)
            else:
                current_user = User.objects.filter(id=int(instance.current_user_id)).first()
                broker = Broker.objects.filter(id=current_user.profile.broker_id if current_user and current_user.profile else None).first()
        
            profile = Profile.objects.create(user=creating_user, account_type=account_type, broker=broker)
            if not profile.broker:
                Profile.objects.filter(id=profile.id).update(broker=broker)
            is_super_admin = False
            if (account_type and account_type.name == AccountTypeEnum.BUSINESS_ADMIN.value) or creating_user.is_superuser:
                is_super_admin = True
            Profile.objects.filter(id=profile.id).update(is_super_admin=is_super_admin)
            print(5555)
        except Exception as e:
            print("Getting create_user_profile error as message: ", e)
        


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()