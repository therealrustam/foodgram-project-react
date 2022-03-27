from django.contrib import admin
from users.models import User

from .models import (Cart, Favorite, Follow, Ingredient, IngredientRecipe,
                     Recipe, Tag, TagRecipe)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
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
    list_display = ('user', 'recipes')
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
                    'cooking_time',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
