from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import User

from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer,
                          RegistrationSerializer, SubscribeSerializer,
                          TagSerializer)


class CreateUserView(UserViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

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
        subscribe = Subscribe.objects.filter(following=request.user)
        print(request.user.id)
        queryset = subscribe.authors.all()
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeWriteSerializer
        return RecipeReadSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


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


class DownloadViewSet():
    pass
