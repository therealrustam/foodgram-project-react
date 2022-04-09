"""
Настройка админ зоны проекта Foodgram.
"""

from django.contrib import admin

from users.models import User
from .models import (Cart, Favorite, Subscribe, Ingredient, IngredientRecipe,
                     Recipe, Tag, TagRecipe)


class IngredientRecipeInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели ингредиентов в рецепте.
    """
    model = IngredientRecipe
    extra = 0


class TagRecipeInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели тэгов рецепта.
    """
    model = TagRecipe
    extra = 0


class UserAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны пользователя.
    """
    list_display = ('username', 'email', 'id')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    list_filter = ('username',)


class IngredientAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны продуктов.
    """
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны тэгов.
    """
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class CartAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны продуктовой корзины.
    """
    list_display = ('user', 'recipes', 'id')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class FavoriteAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны избранных рецептов.
    """
    list_display = ('user', 'recipes')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class RecipeAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны рецептов.
    """
    inlines = (IngredientRecipeInline, TagRecipeInline,)
    list_display = ('name', 'author', 'text',
                    'cooking_time', 'id', 'pub_date')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class SubscribeAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны.
    """
    list_display = ('user', 'following')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
