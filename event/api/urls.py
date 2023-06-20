from django.urls import path

from ..api import views


urlpatterns = [
    path("get_sub_category/", views.SubCategoryListAPIView.as_view(), name="get_subcategory_list"),
    path("get_sub_category_event/<int:event_id>/", views.SubCategoryEventListAPIView.as_view(), name="get_subcategory_event_list"),
    path("sub_category/", views.SubCategoryAPIView.as_view(), name="list_create_subcategory_event"),
    path("sub_category/<int:pk>/", views.SubCategoryRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_subcategory_event"),
    path("get_event/", views.EventListAPIView.as_view(), name="get_event_list"),
    path("event/", views.EventAPIView.as_view(), name="list_create_event"),
    path("event/<int:pk>/", views.EventRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_event"),
]