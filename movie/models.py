from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250)
    show_date = models.DateField(null=True, blank=False)
    time_show_date = models.TimeField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=False)
    time_close_date = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)
    notification = models.CharField(max_length=250, null=True, blank=True)

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
    