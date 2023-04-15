from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Review(models.Model):
    SCORE_CHOICES = [(1, '1'), (2, '2'),
                     (3, '3'), (4, '4'),
                     (5, '5'), (6, '6'),
                     (7, '7'), (8, '8'),
                     (9, '9'), (10, '10')]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.SmallIntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='rating_once'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.text
