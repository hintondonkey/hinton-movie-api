from django.urls import path
from movie.api.views import GetAllStreamPlatformAV
from movie.api.views import WatchListAV, WatchListDetailAV, StreamPlatformAV, UpdateNotificationAV, GetNotification, StreamPlatformDetailAV, GetStreamPlatformDetailAV

urlpatterns = [
    path('liststream/', GetAllStreamPlatformAV.as_view(), name='list-streamplatform'),  
    path('<int:pk>', GetStreamPlatformDetailAV.as_view(), name='streamplatform-detail'),

    
    path('noti/<int:pk>', UpdateNotificationAV.as_view(), name='update-notification'),
    path('get-noti/<int:pk>', GetNotification.as_view(), name='get-notification'),
    path('stream/', StreamPlatformAV.as_view(), name='Streamplatform-list'), 
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='Streamplatform-details'),
    path('watch-list/', WatchListAV.as_view(), name='Streamplatform-list'), 
    path('watch-list/<int:pk>', WatchListDetailAV.as_view(), name='Streamplatform-details'),
    # path('list/', StreamPlatform_list, name="StreamPlatform_list"),
    # path('<int:pk>', StreamPlatform_details, name="StreamPlatform_details")

]