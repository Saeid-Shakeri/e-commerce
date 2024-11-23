from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views # type: ignore

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'), # for login
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),
    path('login/', login, name='login'),
    path('index/', index, name='index'),
    path('product/<int:pk>/', product, name="product"),

    path('resetpass/',resetpass, name='resetpass'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', edit_profile, name='edit_profile'),
    path('dashboard/password/', change_password, name='change_password'),
    path('message/', message, name="message"),
    path('support/', support, name="support"),
    path('logout/', logout, name="logout")



]