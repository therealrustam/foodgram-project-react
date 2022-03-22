from django.contrib import admin

from .models import Follow, Ingredient, Recipe, Tag
from users.models import User


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


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text',
                    'cooking_time', 'tag', 'ingredient')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
