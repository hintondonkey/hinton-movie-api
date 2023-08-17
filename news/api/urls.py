from django.urls import path

from ..api.views import *


urlpatterns = [
    path("get_news_list/<int:broker_id>/", NewsBrokerListAPIView.as_view(), name="get_news_list"),
    path("get_news_list/<int:broker_id>/<int:category_id>/", NewsListAPIView.as_view(), name="get_news_list"),
    path("get_news_list/<int:broker_id>/<int:category_id>/<int:subcategory_id>/", NewsCategoryBrokerSubCategoryListAPIView.as_view(), name="get_sub_news_list"),
    path('<int:broker_id>/<int:pk>/', NewsAPIView.as_view(), name='get_news_broker_detail'),
    path('news/', NewsCreateAPIView.as_view(), name='create_news'),
    # path('news_update_active/<int:pk>/', StreamPlatformActiveUpdateAPIView.as_view(), name='news_update_active'),
    # path("news/", NewsAPIView.as_view(), name="list_create_news"),
    path("news/<int:pk>/", NewsRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_news"),
]