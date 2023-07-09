from django.urls import path

from ..api.views import *


urlpatterns = [
    path('get_notification_event_list/<int:stream_platform_id>/', NotificationEventListAPIView.as_view(), name='get_notification_event_list'),
    path('<int:pk>/', NotificationRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy_notification'),
    path("notificaiton/", NotificationCreateAPIView.as_view(), name="create_notification"),

]