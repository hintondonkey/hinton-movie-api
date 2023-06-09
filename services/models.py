
from django.conf import settings
from django.db import models

from lookup.models import Category, BaseCreateModel
from user_app.models import User, Broker


class SubCategory(BaseCreateModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='parent_subcategory')
    created_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='user_create_subcategory')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True, related_name='broker_subcategory')

    def __str__(self):
        return self.name
    
    @property
    def total_stream_platform(self):
        num = 0
        try:
            num = self.stream_platform_subcaterogy.count()
        except Exception as e:
            num = 0
            print(e)
        return num
    
    
class BrokerService(BaseCreateModel):
    name = models.TextField(default='', null=True, blank=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)




