
from django.conf import settings
from django.db import models

from lookup.models import Category, BaseCreateModel
from services.models import SubCategory
from user_app.models import User, Broker

    
class News(BaseCreateModel):
    title = models.CharField(max_length=250)
    short_content = models.TextField(null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    post_date = models.DateField(null=True, blank=False)
    post_time = models.TimeField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=False)
    event_time = models.TimeField(null=True, blank=True)
    end_event_date = models.DateField(null=True, blank=False)
    end_event_time = models.TimeField(null=True, blank=True)
    approval = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    is_horizontal = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='news_caterogy')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, related_name='news_subcaterogy')
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_create_news')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True, related_name='broker_news')


class MultipleImage(models.Model):
    uid = models.CharField(max_length=250)
    name = models.CharField(max_length=250, null=True, blank=False)
    description = models.TextField(null=False, blank=False)
    file = models.CharField(max_length=250, null=True, blank=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_image')




