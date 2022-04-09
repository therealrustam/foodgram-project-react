"""
Создание необходимых моделей.
"""

from wsgiref.validate import validator
from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Ingredient(models.Model):
    """
    Создание модели продуктов.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название продуктов')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Введите единицы измерения')

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return self.name


class Tag(models.Model):
    """
    Создание модели тэгов.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название тега')
    color = ColorField(
        format='hex',
        verbose_name='Цвет',
        help_text='Введите цвет тега')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Текстовый идентификатор тега',
        help_text='Введите текстовый идентификатор тега')

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return self.slug


class Recipe(models.Model):
    """
    Создание модели рецептов.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Выберите автора рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        blank=True,
        help_text='Выберите изображение рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описания рецепта')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления',
        help_text='Введите время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тег рецепта',
        help_text='Выберите тег рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Продукты в рецепте',
        help_text='Выберите продукты рецепта')
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='Избранный рецепт',
        help_text='Добавить рецепт в избранные')
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='Продукты рецепта в корзину',
        help_text='Добавить продукты рецепта в корзину'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Добавить дату создания')

    class Meta:
        """
        Мета параметры модели.
        """
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return self.name


class Cart(models.Model):
    """
    Создание модели корзины.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты',
        help_text='Выберите рецепты для добавления в корзины'
    )

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.user} {self.recipes}'


class Subscribe(models.Model):
    """
    Создание модели подписок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются'
    )

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.user} {self.following}'


class IngredientRecipe(models.Model):
    """
    Создание модели продуктов в рецепте.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Продукты рецепта',
        help_text='Добавить продукты рецепта в корзину')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество продукта',
        help_text='Введите количество продукта'
    )

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Продукты в рецепте'
        verbose_name_plural = 'Продукты в рецепте'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    """
    Создание модели тегов рецепта.
    """
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Выберите теги рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    """
    Создание модели избранных рецептов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipes'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.recipes} {self.user}'
