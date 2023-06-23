
from django.conf import settings
from django.db import models

from lookup.models import Category, BaseCreateModel
from user_app.models import User, Broker


class SubCategory(BaseCreateModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parent_subcategory')
    created_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_create_subcategory')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True, related_name='broker_subcategory')

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
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)




