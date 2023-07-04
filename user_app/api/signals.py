from django.dispatch import receiver
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage

from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import *
from services.models import BrokerService
from lookup.models import Category
from hintonmovie.globals import *
from hintonmovie.settings import EMAIL_HOST_USER


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
            business_type = None
            
            creating_user = User.objects.filter(id=instance.id).first()
            try:
                account_type = AccountType.objects.filter(name=instance.account_type).first()
            except Exception as e:
                print("Getting account_type_name error as message: ", e)
            try:
                business_type = BusinessType.objects.filter(name=instance.business_type).first()
            except Exception as e:
                print("Getting business_type error as message: ", e)


            if (account_type and account_type.name == AccountTypeEnum.BUSINESS_ADMIN.value) or creating_user.is_superuser:
                broker = Broker.objects.create(name=creating_user.username, is_network=creating_user.is_superuser, business_type=business_type)
            else:
                current_user = User.objects.filter(id=int(instance.current_user_id)).first()
                broker = Broker.objects.filter(id=current_user.profile.broker_id if current_user and current_user.profile else None).first()
            
            profile = Profile.objects.create(user=creating_user, account_type=account_type, broker=broker, is_active=creating_user.is_superuser)
            
            if not profile.broker:
                Profile.objects.filter(id=profile.id).update(broker=broker)
            is_super_admin = False
            if (account_type and account_type.name == AccountTypeEnum.BUSINESS_ADMIN.value) or creating_user.is_superuser:
                is_super_admin = True
            Profile.objects.filter(id=profile.id).update(is_super_admin=is_super_admin)

            
            try:
                profile = Profile.objects.filter(id=profile.id).first()
                if profile and profile.account_type:
                    email_from = EMAIL_HOST_USER
                    full_name = str(profile.user.first_name) + ' ' + str(profile.user.last_name)
                    message_subject =  "Hinton Movie created new {account_type} for {title}".format(account_type=profile.account_type.name, title=full_name)
                    msg_content = "<!DOCTYPE html><body><br><p>Hi {full_user_name}<p><h2>Thank you for your registration.</h2><h3>Your Account:</h3> <p>Username: {user_name} </p></br> <p>Password: {password} </p><br/>"
                    msg_content = msg_content + "<p>Please click on the following link to active your account first:</p>"
                    msg_content = msg_content + "<a href='"
                    msg_content = msg_content + "https://hintondonkey.com{}?username={}&id={}".format(reverse('user_active'), str(creating_user.username), str(creating_user.id))
                    msg_content = msg_content + "'\">" + "https://hintondonkey.com{}?username={}&id={}".format(reverse('user_active'), str(creating_user.username), str(creating_user.id)) + "</a>"
                    msg_content = msg_content + "</body></html>"
                    msg_content = msg_content.format(full_user_name=full_name, user_name=profile.user.username, password=instance.password2)

                    email_to = [profile.user.email]
                    
                    msg = EmailMessage(message_subject, msg_content, email_from, to=email_to)

                    msg.content_subtype = 'html'
                    msg.mixed_subtype = 'related'
                    msg.send()
            except Exception as e:
                print("Getting error while sending email for new Business Admin Account as message: ", e)

            try:
                
                for category in Category.objects.all():
                    name = category.name + ' Management'
                    if not BrokerService.objects.filter(name=name, broker=broker).exists():
                        BrokerService.objects.create(name=name, broker=broker, category=category, price=10)
                account_management = 'Account Management'
                if not BrokerService.objects.filter(name=account_management, broker=broker).exists():
                    BrokerService.objects.create(name=account_management, broker=broker, category=None, price=10)

            except Exception as e:
                print("Getting create_broker_service error as message: ", e)

        except Exception as e:
            print("Getting create_user_profile error as message: ", e)
        


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "https://hintondonkey.com{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    email_from = EMAIL_HOST_USER
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Hinton Movie"),
        # message:
        email_plaintext_message,
        # from:
        email_from,
        # to:
        [reset_password_token.user.email]
    )