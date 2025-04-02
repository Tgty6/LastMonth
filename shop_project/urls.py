from django.contrib import admin
from django.urls import path, include
from users import views
from . import swagger


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/users/', include('users.urls')),
    path('registration/', views.registration_api_view),
    path('authorization/', views.AuthAPIView.as_view())
]

urlpatterns += swagger.urlpatterns