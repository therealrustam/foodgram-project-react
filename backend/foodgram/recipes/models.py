from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Ingredient(models.Model):
    """
    Создание модели продуктов.
    """
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Tag(models.Model):
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
        related_name='recipes',
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
    )


class Follow(models.Model):
    """
    Модель подписок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
