from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.generics import CreateAPIView
from users.models import User

from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, RegistrationSerializer,
                          TagSerializer)


class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass
