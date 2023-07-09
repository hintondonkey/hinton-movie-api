
from django.conf import settings
from django.db import models

from lookup.models import BaseCreateModel
from user_app.models import User
from movie.models import StreamPlatform

    
class Notification(BaseCreateModel):
    title = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_create_notification')
    stream_platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, null=True, related_name='stream_platform_notification')




