"""
Настройка пользовательских фильтров.
"""

from django_filters import rest_framework
from rest_framework import filters

from recipes.models import Recipe
from users.models import User


class RecipeFilters(rest_framework.FilterSet):
    """
    Настройка фильтров модели рецептов.
    """
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        """
        Мета параметры фильтров модели рецептов.
        """
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        """
        Метод обработки фильтров параметра is_favorited.
        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """
        Метод обработки фильтров параметра is_in_shopping_cart.
        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset.all()


class IngredientSearchFilter(filters.SearchFilter):
    """
    Настройка фильтра поиска модели продуктов.
    """
    search_param = 'name'
