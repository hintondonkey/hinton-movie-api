
from django.conf import settings
from django.db import models

from lookup.models import Category, BaseCreateModel
from user_app.models import User, Broker


class SubCategory(BaseCreateModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parent_subcategory')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_create_subcategory')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='broker_subcategory')



