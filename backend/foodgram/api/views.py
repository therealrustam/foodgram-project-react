from djoser.views import UserViewSet
from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import User

from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, RegistrationSerializer,
                          TagSerializer)


class CreateUserView(UserViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Класс вьюсет подписок.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


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
