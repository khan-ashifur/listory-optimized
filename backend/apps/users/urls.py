from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileView, LoginView, RegisterView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]