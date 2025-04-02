from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ProductListCreateAPIView,
                    CategoryListCreateAPIView,
                    CategoryDetailAPIView, TagViewSet,
                    )

router = DefaultRouter()
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('api/v1/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),

    path('api/v1/categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('api/v1/categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),


    path('api/v1/', include(router.urls)),
]
