from django.urls import path

from ..api import views


urlpatterns = [
    path("category/", views.CategoryAPIView.as_view(), name="list-create-category"),
    
]