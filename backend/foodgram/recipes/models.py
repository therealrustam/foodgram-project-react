from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredients(models.Model):
    """
    Создание модели продуктов.
    """
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Tags(models.Model):
    """
    Создание модели тэгов.
    """
    name = models.CharField(max_length=200)
    color = ColorField(format='hex')
    slug = models.SlugField(max_length=200, unique=True)


class Recipe(models.Model):
    """
    Создание модели рецептов.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField(min=1)
    tags = models.ForeignKey(
        Tags,
        related_name='recipes'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        related_name='recipes'
    )
