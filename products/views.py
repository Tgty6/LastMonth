from collections import OrderedDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Tag, Movie, Director
from .serializers import (ProductSerializer,
                          ProductDetailSerializer,
                          ProductValidateSerializer,
                          CategorySerializer,
                          TagSerializer,MovieSerializer,
                          DirectorSerializer)
from django.db import transaction
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))



class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('tags', 'reviews').filter(is_active=True)
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        products = self.get_queryset()

        data = ProductSerializer(instance=products, many=True).data
        return Response(data=data)

    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

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

        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


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



class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

        data = self.get_serializer(product).data
        return Response(data=data)

    def delete(self, request, *args, **kwargs):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)


        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.name = serializer.validated_data.get('name')
        product.text = serializer.validated_data.get('text')
        product.category_id = serializer.validated_data.get('category_id')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()

        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_200_OK)


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all().annotate(movies_count=Count('movies'))
    serializer_class = DirectorSerializer

    def post(self, request, *args, **kwargs):
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'
