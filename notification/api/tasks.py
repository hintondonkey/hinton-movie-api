import firebase_admin
from firebase_admin import credentials, messaging
from django.db.models import Q
from django.db.models import F, Value, DateTimeField, ExpressionWrapper
from datetime import datetime, timedelta
from hintonmovie.permissions import *
from hintonmovie.globals import *

from notification.models import Notification
from hintonmovie.globals import *
from celery import shared_task

creds = credentials.Certificate("movie/api/cert.json")
firebase_admin.initialize_app(creds)


def send_notification(topic, data, title, content):
    try:
        if title and content:
            message = messaging.Message(
                notification=messaging.Notification(title=title, 
                                                        body=content),
                topic=topic,
                data=data
            )
            messaging.send(message)
    except Exception as e:
        print("Error while send notification as message: ", e)


@shared_task
def send_notification_task():
    try:
        now = datetime.now()
        today = now.date()
        a_30_minutes_ago = now - timedelta(minutes=30)
        a_time_30_minutes_ago = a_30_minutes_ago.time()
        a_date_1_day_ago = now.date() - timedelta(days=1)
        notification_list = Notification.objects.filter(status=False, stream_platform__approval=True, stream_platform__status=True, stream_platform__post_date__isnull=False, stream_platform__post_time__isnull=False).filter(Q(stream_platform__post_date__lt=a_date_1_day_ago) | (Q(stream_platform__post_date=today) & Q(stream_platform__post_time__lt=a_time_30_minutes_ago)) | (Q(stream_platform__post_date=a_date_1_day_ago) & (Q(stream_platform__post_time__lte=a_time_30_minutes_ago) | Q(stream_platform__post_time__gte=a_time_30_minutes_ago))))
        for notification in notification_list.iterator():
            send_notification("demo", notification.stream_platform_id, notification.title, notification.content)
            Notification.objects.filter(id=notification.id).update(status=True)
    except Exception as e:
        print("Error while send_notification_task as message: ", e)