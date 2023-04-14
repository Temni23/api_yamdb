from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='titles'
    )
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name
