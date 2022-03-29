from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=150, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.first_name+self.last_name

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username
