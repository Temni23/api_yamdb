from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField("Биография", blank=True)
    role = models.CharField("Роль пользователя", max_length=255, default="user")
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Код подтверждения',
    )

    def __str__(self):
        return self.username
