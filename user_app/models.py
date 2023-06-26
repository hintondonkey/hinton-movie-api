
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from hintonmovie.models import BaseCreateModel
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    account_type = ''
    current_user_id = None
    password2 = None

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
    

class BusinessType(BaseCreateModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Broker(BaseCreateModel):
    name = models.TextField(default='', blank=True)
    is_network = models.BooleanField(default=False)
    number_of_users = models.IntegerField(default=0)
    busines_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)


class AccountType(BaseCreateModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(BaseCreateModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, db_index=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True)
    is_super_admin = models.BooleanField(default=False)
    avatar = models.CharField(max_length=250, null=True, default='')
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, default='')
    street = models.CharField(max_length=100, default='', null=True, blank=True)
    city = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(max_length=100, default='', null=True, blank=True)
    organization = models.CharField(max_length=100, default='', null=True, blank=True)

