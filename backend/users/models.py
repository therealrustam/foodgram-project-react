""""
Создание модели пользователя.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Создание своей модели пользователя.
    """
    username = models.CharField(db_index=True, max_length=150, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        """Строковое представление модели (отображается в консоли)."""
        return self.username

    def get_full_name(self):
        """
        Этот метод возвращает имя и фамилию пользователя.
        """
        return self.first_name+self.last_name

    def get_short_name(self):
        """Этот метод возвращает username пользователя."""
        return self.username
