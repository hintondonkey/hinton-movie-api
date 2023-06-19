from django.urls import path

from ..api import views


urlpatterns = [
    path("get_category_list/", views.CategoryListAPIView.as_view(), name="list-category"),
    path("category/<int:pk>/", views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name="get-update-delete-category"),
    path("list_create_category/", views.CategoryListCreateAPIView.as_view(), name="list-create-category"),
]