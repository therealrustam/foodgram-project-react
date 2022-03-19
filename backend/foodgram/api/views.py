from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework import filters, status, views, viewsets

from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class UserViewSet(viewsets.ModelViewSet):
    pass


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    pass


class IngredientViewSet(viewsets.ModelViewSet):
    pass


class CartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass
