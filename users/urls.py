from django.urls import path
from .views import RegistrationAPIView, UserDetailAPIView
from users import views
urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('user/', UserDetailAPIView.as_view(), name='user-detail'),
    path('authorization/', views.AuthAPIView.as_view()),
]
