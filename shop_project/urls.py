from django.contrib import admin
from django.urls import path, include
from products.views import MovieDetailAPIView, DirectorListCreateAPIView, DirectorDetailAPIView

from . import swagger


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/movies/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('api/v1/movies/<int:id>/', MovieDetailAPIView.as_view(), name='movie-detail'),

    path('api/v1/directors/', DirectorListCreateAPIView.as_view(), name='director-list-create'),
    path('api/v1/directors/<int:id>/', DirectorDetailAPIView.as_view(), name='director-detail'),

]

urlpatterns += swagger.urlpatterns