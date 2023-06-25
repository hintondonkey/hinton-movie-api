from django.contrib import admin
from .models import AccountType, Broker, BusinessType

# Register your models here.
admin.site.register(AccountType)
admin.site.register(Broker)
admin.site.register(BusinessType)
