from django.urls import path
from products import views
from utils.constants import LIST_CREATE, RETRIEVE_UPDATE_DESTROY


urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view()),
    path('<int:id>/', views.product_detail_api_view),
    path('categories/', views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('tags/', views.TagViewSet.as_view(LIST_CREATE)),
    path('tags/<int:id>/', views.TagViewSet.as_view(RETRIEVE_UPDATE_DESTROY)),
]
