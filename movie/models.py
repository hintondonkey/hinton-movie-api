from django.db import models
from user_app.models import User, Broker
from lookup.models import Category
from services.models import SubCategory


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return '{filename}'.format(filename=filename)
    

# Create your models here.
class StreamPlatform(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    sub_icon = models.CharField(max_length=250, null=True, blank=True)
    uid_sub_icon = models.CharField(max_length=250, null=True, blank=True)
    show_date = models.DateField(null=True, blank=False)
    time_show_date = models.TimeField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=False)
    time_close_date = models.TimeField(null=True, blank=True)
    post_date = models.DateField(null=True, blank=False)
    post_time = models.TimeField(null=True, blank=True)
    close_post_date = models.DateField(null=True, blank=False)
    close_post_time = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)
    titleNoti = models.CharField(max_length=250, null=True, blank=True)
    summaryNoti = models.TextField(null=True, blank=True)
    number_of_connection = models.IntegerField(default=0, blank=True, null=True)
    approval = models.CharField(max_length=250, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_horizontal = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, related_name='stream_platform_caterogy')
    subcategory = models.ManyToManyField(SubCategory, null=True, related_name='stream_platform_subcaterogy')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True, related_name='stream_platform_broker')

    def str (self):
        return self.title


class WatchList(models.Model):
    date_picker = models.DateField(null=False, blank=False)
    time_show_date = models.TimeField(null=False, blank=False)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    price = models.IntegerField(default=0)
    website = models.URLField(max_length=100)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def str (self):
        return self.platform.title
    

class MultipleImage(models.Model):
    uid = models.CharField(max_length=250)
    name = models.CharField(max_length=250, null=True, blank=False)
    file_name = models.CharField(max_length=250, null=True, blank=False)
    file_size = models.CharField(max_length=250, null=True, blank=False)
    description = models.TextField(null=False, blank=False)
    event = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='stream_platform_image')




    