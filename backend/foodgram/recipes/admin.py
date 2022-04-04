"""
Настройка админ зоны проекта Foodgram.
"""

from django.contrib import admin

from users.models import User
from .models import (Cart, Favorite, Subscribe, Ingredient, IngredientRecipe,
                     Recipe, Tag, TagRecipe, ShoppingCart)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    list_filter = ('username',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes', 'id')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline, TagRecipeInline,)
    list_display = ('name', 'author', 'text',
                    'cooking_time', 'id', 'pub_date')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'user')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'
    list_filter = ('ingredient',)


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
