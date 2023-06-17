from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenBlacklistView


from ..api import views


# from user_app.api.views import 
urlpatterns = [
    # path('login/', obtain_auth_token, name='login'), 
    # path('register/', registration_view, name='register'), 
    # path('logout/', logout_view, name='logout')
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path("subuser/", views.SubUserRegisterationAPIView.as_view(), name="sub-user"),
    
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/avatar/", views.UserAvatarAPIView.as_view(), name="user-avatar"),
]