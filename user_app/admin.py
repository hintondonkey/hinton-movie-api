from django.contrib import admin
from .models import AccountType, Broker

# Register your models here.
admin.site.register(AccountType)
admin.site.register(Broker)
