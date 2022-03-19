from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


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
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    tags = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        blank=True,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        blank=True,
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
