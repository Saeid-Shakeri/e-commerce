from django.urls import path
from .views import (CustomerRegisterView, ProfileView, 
                    ChangePasswordView, ChangeEmailView)
from rest_framework_simplejwt import views as jwt_views # type: ignore

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'), # for login
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),
]