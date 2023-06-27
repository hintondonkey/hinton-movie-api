from django.urls import path

from ..api import views


urlpatterns = [
    path("get_sub_category/", views.SubCategoryListAPIView.as_view(), name="get_subcategory_list"),
    path("get_sub_category/<int:category_id>/", views.SubCategoryListCategoryAPIView.as_view(), name="get_subcategory_list_category"),
    path("sub_category/", views.SubCategoryAPIView.as_view(), name="list_create_subcategory_event"),
    path("sub_category/<int:pk>/", views.SubCategoryRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_subcategory_event"),
    path("broker_service/<int:pk>/", views.BrokerServiceAPIView.as_view(), name="get_update_broker_service"),
    path("get_category_list/<int:broker_id>/", views.CategoryBrokerListAPIView.as_view(), name="list_broker_category"),
    path("get_broker_service/<int:broker_id>/", views.BrokerServiceListAPIView.as_view(), name="get_broker_service_list"),
    path("get_broker_service_business_admin/", views.BrokerServiceBAListAPIView.as_view(), name="get_broker_service_business_admin"),
    
]