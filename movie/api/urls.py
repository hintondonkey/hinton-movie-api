from django.urls import path
from movie.api.views import *


urlpatterns = [
    path('liststream/', GetAllStreamPlatformAV.as_view(), name='list-streamplatform'),
    path('liststream/<int:broker_id>/<int:category_id>/', StreamPlatformCategoryBrokerListAPIView.as_view(), name='list_stream_platform_category_broker'),
    path('liststream/<int:broker_id>/', StreamPlatformBrokerListAPIView.as_view(), name='list_stream_platform_broker'), 
    path('<int:pk>', GetStreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('<int:pk>', StreamPlatformAPIView.as_view(), name='get_stream_platform'),
    path('stream_platform/<int:pk>/', StreamPlatformRetrieveUpdateDestroyAPIView.as_view(), name='get_update_delete_stream_platform'),
    path('noti/<int:pk>', UpdateNotificationAV.as_view(), name='update-notification'),
    path('get-noti/', GetNotification.as_view(), name='get-notification'),
    path('stream/', StreamPlatformAV.as_view(), name='Streamplatform-list'),
    path('update_number_of_connection_stream/', NumberOfConnectionMovieUpdateAPIView.as_view(), name='update_number_of_connection_stream'),
    path('poststream/', StreamPlatPostformAV.as_view(), name='StreamplatformPost-list'), 
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='Streamplatform-details'),
    path('watch-list/', WatchListAV.as_view(), name='Streamplatform-list'),
    path('watch-list/platform/<int:pk>', GetWatchListByPlatformIdAV.as_view(), name='get-platform-list-by-platform-id'),
    path('watch-list/<int:pk>', WatchListDetailAV.as_view(), name='Streamplatform-details'),
]




