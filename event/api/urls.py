from django.urls import path

from ..api import views


urlpatterns = [
    path("sub_category/", views.SubCategoryAPIView.as_view(), name="list-create-subcategory-event"),
    path("event/", views.EventAPIView.as_view(), name="list-create-event"),
]