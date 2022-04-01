from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag
from rest_framework import (filters, mixins, pagination, permissions, status,
                            views, viewsets)
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import User

from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, RegistrationSerializer,
                          SubscribeSerializer, TagSerializer)


class CreateUserView(UserViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination

    def list(self, request):
        queryset = User.objects.all()
        serializer = RegistrationSerializer(queryset, many=True)
        return Response(serializer.data)


class SubscribeViewSet(viewsets.ModelViewSet):
    """
    Класс вьюсет подписок.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = get_list_or_404(User, following__user=self.request.user)
        serializer = RegistrationSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=author_id, following__id=user_id)
        subscribe.delete()
        return Response(status=204)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'is_favorited', 'is_in_shopping_cart', 'author', 'tags')
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeWriteSerializer
        return RecipeReadSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('^name',)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        recipes_id = self.kwargs['recipes_id']
        user_id = request.user.id
        cart = get_object_or_404(
            Cart, user__id=user_id, recipes__id=recipes_id)
        cart.delete()
        return Response(status=204)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        recipes_id = self.kwargs['recipes_id']
        user_id = request.user.id
        favorite = get_object_or_404(
            Favorite, user__id=user_id, recipes__id=recipes_id)
        favorite.delete()
        return Response(status=204)


class DownloadViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def list(self, request):
        print(1)
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)
