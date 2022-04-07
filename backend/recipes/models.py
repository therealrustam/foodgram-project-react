"""
Создание необходимых моделей.
"""

from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Ingredient(models.Model):
    """
    Создание модели продуктов.
    """
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единицы измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Tag(models.Model):
    """
    Создание модели тэгов.
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    color = ColorField(format='hex', verbose_name='Цвет')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    """
    Создание модели рецептов.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='static/images/recipes/',
        blank=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', related_name='recipes')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Cart(models.Model):
    """
    Создание модели корзины.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
    )

    def __str__(self):
        return f'{self.user} {self.recipes}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Subscribe(models.Model):
    """
    Создание модели подписок.
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

    def __str__(self):
        return f'{self.user} {self.following}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow')
        ]


class IngredientRecipe(models.Model):
    """
    Создание модели продуктов в рецепте.
    """
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredientrecipes')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredientrecipes')
    amount = models.IntegerField(default=1,
                                 validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'

    class Meta:
        verbose_name = 'Продукты в рецепте'
        verbose_name_plural = 'Продукты в рецепте'


class TagRecipe(models.Model):
    """
    Создание модели тегов рецепта.
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тэги рецепта'
        verbose_name_plural = 'Тэги рецепта'


class Favorite(models.Model):
    """
    Создание модели избранных рецептов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    def __str__(self):
        return f'{self.recipes} {self.user}'

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
