from collections import OrderedDict


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Tag, Movie, Director, Reviews
from .serializers import (ProductSerializer,
                          ProductDetailSerializer,
                          ProductValidateSerializer,
                          CategorySerializer,
                          TagSerializer,
                          MovieSerializer,
                          DirectorSerializer)
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg, Count


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = (Product.objects.select_related('category')
                .prefetch_related('tags', 'reviews').filter(is_active=True))
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = serializer.validated_data.get('name')
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        with transaction.atomic():
            product = Product.objects.create(
                name=name,
                text=text,
                price=price,
                is_active=is_active,
                category_id=category_id,
            )
            product.tags.set(tags)
            product.save()

        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'


@api_view(['GET'])
def movie_list_reviews_api_view(request):
    movies = Movie.objects.prefetch_related('reviews').annotate(
        rating=Avg('reviews__stars')
    )
    data = MovieSerializer(movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.annotate(movies_count=Count('movies'))
    data = DirectorSerializer(directors, many=True).data
    return Response(data=data)


def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.name = serializer.validated_data.get('name')
        product.text = serializer.validated_data.get('text')
        product.category_id = serializer.validated_data.get('category_id')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)

