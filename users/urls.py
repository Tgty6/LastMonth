from django.urls import path
from .views import RegistrationAPIView, UserDetailAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('user/', UserDetailAPIView.as_view(), name='user-detail'),]
