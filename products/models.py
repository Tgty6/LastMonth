from django.db import models

class AbstractNameModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(AbstractNameModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True)


class Tag(AbstractNameModel):
    pass


class Director(AbstractNameModel):
    pass


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.stars for review in reviews) / reviews.count()
        return 0


STARS = [(i, str(i)) for i in range(1, 6)]

class Review(models.Model):
    text = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=5)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.movie.name} - {self.stars} stars'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def category_name(self):
        return self.category.name if self.category else None

class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField()