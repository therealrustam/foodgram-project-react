from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import Ingredients, Recipe, Tags


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text',
                    'cooking_time', 'tags', 'ingredients')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipe, RecipeAdmin)
