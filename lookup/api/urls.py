from django.urls import path

from ..api import views


urlpatterns = [
    path("get_category_list/", views.CategoryListAPIView.as_view(), name="list_category"),
    path("category/", views.CategoryListCreateAPIView.as_view(), name="list_create_category"),
    path("category/<int:pk>/", views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_category"),
]