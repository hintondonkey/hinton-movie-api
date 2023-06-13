
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BaseCreateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Broker(BaseCreateModel):
    name = models.TextField(default='', blank=True)
    is_network = models.BooleanField(default=False)
    number_of_users = models.IntegerField(default=0)


class AccountType(BaseCreateModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)


class Profile(BaseCreateModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, db_index=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True)
    is_super_admin = models.BooleanField(default=False)
    avatar = models.ImageField(verbose_name="Avatar", blank=True, null=True)
    website = models.URLField(default='', null=True, blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, default='')
    street = models.CharField(max_length=100, default='', null=True, blank=True)
    city = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(max_length=100, default='', null=True, blank=True)
    organization = models.CharField(max_length=100, default='', null=True, blank=True)
