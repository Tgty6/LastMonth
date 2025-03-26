from django.contrib import admin
from django.urls import path, include
from products.views import movie_list_reviews_api_view, director_list_api_view
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/movies/reviews/', movie_list_reviews_api_view),
    path('api/v1/directors/', director_list_api_view),

    path('registration/', views.registration_api_view),
    path('authorization/', views.AuthAPIView.as_view())
]
