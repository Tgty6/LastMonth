from django.contrib import admin
from .models import Product, Category, Tag, Movie, Director, Review


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Review)