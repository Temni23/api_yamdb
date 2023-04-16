from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    bio = models.TextField("Биография", blank=True)
    role = models.CharField("Роль пользователя", max_length=25, choices=ROLE_CHOICES,
                            default=USER)
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Код подтверждения',
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
