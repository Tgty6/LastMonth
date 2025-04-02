from rest_framework import serializers
from .models import Product, Category, Tag, Movie, Director, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id name price created category category_name tags tag_names reviews'.split()
        depth = 1

    def get_tag_names(self, product):
        return [tag.name for tag in product.tags.all()]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=3, max_length=255)
    text = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=1, max_value=1000000)
    is_active = serializers.BooleanField(default=False)
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

    def validate_tags(self, tags):
        tags = list(set(tags))
        tags_db = Tag.objects.filter(id__in=tags)
        if len(tags_db) != len(tags):
            raise ValidationError('Tag does not exist')
        return tags

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Movie
        fields = 'id name reviews rating'.split()

    def validate_title(self, value):
        if Movie.objects.filter(title=value).exists():
            raise serializers.ValidationError("Фильм с таким названием уже существует.")
        return value

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

    def validate_name(self, value):
        if Director.objects.filter(name=value).exists():
            raise serializers.ValidationError("Режиссер с таким именем уже существует.")
        return value


