from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ProductListCreateAPIView,
                    CategoryListCreateAPIView,
                    CategoryDetailAPIView, TagViewSet,
                    MovieDetailAPIView, DirectorListCreateAPIView,
                    DirectorDetailAPIView)

router = DefaultRouter()
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('', include(router.urls)),
    path('movies/<int:id>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('directors/', DirectorListCreateAPIView.as_view(), name='director-list-create'),
    path('directors/<int:id>/', DirectorDetailAPIView.as_view(), name='director-detail'),
]