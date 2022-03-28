from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import User

from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
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


class SubscribeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Класс вьюсет подписок.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = Subscribe.objects.all()
        serializer = SubscribeSerializer(queryset, many=True)
        return Response(serializer.data)


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
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


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
