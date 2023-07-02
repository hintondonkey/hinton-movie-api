from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView


from ..api import views


# from user_app.api.views import 
urlpatterns = [
    # path('login/', obtain_auth_token, name='login'), 
    # path('register/', registration_view, name='register'), 
    # path('logout/', logout_view, name='logout')
    path("register/", views.UserRegisterationAPIView.as_view(), name="create_user"),
    path("subuser/", views.SubUserRegisterationAPIView.as_view(), name="sub_user"),
    path("subuser/<int:pk>/", views.SubUserRetrieveUpdateDestroyAPIView.as_view(), name="get_update_delete_sub_user"),
    
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("password_reset/", include('django_rest_passwordreset.urls'), name='password_reset'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout_user"),
    path("", views.UserAPIView.as_view(), name="user_info"),
    path("profile/", views.UserProfileAPIView.as_view(), name="user_profile"),
    path("profile/avatar/", views.UserAvatarAPIView.as_view(), name="user_avatar"),
    path("profile/active/", views.UserActiveAPIView.as_view(), name="user_active"),
    path("account_type/", views.AccountTypeAPIView.as_view(), name="account_type"),
    path("business_type/", views.BusinessTypeAPIView.as_view(), name="business_type"),
    
]