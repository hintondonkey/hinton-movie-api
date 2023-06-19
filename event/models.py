
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
    # broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='broker_subcategory')

    
class Event(BaseCreateModel):
    title = models.CharField(max_length=250)
    summary = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)
    event_date = models.DateField(null=True, blank=False)
    event_time = models.TimeField(null=True, blank=True)
    end_event_date = models.DateField(null=True, blank=False)
    end_event_time = models.TimeField(null=True, blank=True)
    post_date = models.DateField(null=True, blank=False)
    post_time = models.TimeField(null=True, blank=True)
    end_post_date = models.DateField(null=True, blank=False)
    end_post_time = models.TimeField(null=True, blank=True)
    notification_title = models.CharField(max_length=250, null=True, blank=True)
    notification_summary = models.TextField(null=True, blank=True)
    approval = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='event_category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_create_event')


class MultipleImage(models.Model):
    uid = models.CharField(max_length=250)
    name = models.CharField(max_length=250, null=True, blank=False)
    description = models.TextField(null=False, blank=False)
    file = models.CharField(max_length=250, null=True, blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_image')




