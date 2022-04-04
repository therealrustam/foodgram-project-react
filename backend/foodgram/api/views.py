"""
Создание view классов обработки запросов.
"""

import json
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response

from users.models import User
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Subscribe, Tag)
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RegistrationSerializer, ShoppingSerializer,
                          SubscribeSerializer, SubscriptionSerializer,
                          TagSerializer)


class CreateUserView(UserViewSet):
    """
    Вьюсет обработки моделей пользователя.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def list(self, request):
        """
        Метод создание списка пользователей.
        """
        queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RegistrationSerializer(queryset,
                                            many=True,
                                            context={'request': request})
        return Response(serializer.data)


class SubscribeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей подписок.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        Метод создания списка авторов,
        на которых подписан текущий пользователь.
        """
        queryset = get_list_or_404(User, following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления подписок.
        """
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(status=204)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет обработки моделей тэгов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'is_favorited', 'is_in_shopping_cart', 'author', 'tags')
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        """
        Метод подстановки параметров автора при создании рецепта.
        """
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки модели продуктов.
    """
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('^name',)


class CartViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки модели корзины.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления модели корзины.
        """
        recipes_id = self.kwargs['recipes_id']
        user_id = request.user.id
        cart = get_object_or_404(
            Cart, user__id=user_id, recipes__id=recipes_id)
        cart.delete()
        return Response(status=204)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки модели избранных рецептов.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления модели избранных рецептов.
        """
        recipes_id = self.kwargs['recipes_id']
        user_id = request.user.id
        favorite = get_object_or_404(
            Favorite, user__id=user_id, recipes__id=recipes_id)
        favorite.delete()
        return Response(status=204)


class DownloadViewSet(viewsets.ModelViewSet):
    """
    Вьюсет сохранения файла списка покупок.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        Метод создания списка покупок.
        """
        carts = get_list_or_404(
            Cart, user__id=request.user.id)
        recipes = list()
        for cart in carts:
            recipes.append(Recipe.objects.get(carts=cart))
        ingredients = list()
        for recipe in recipes:
            ingredients.extend(
                (IngredientRecipe.objects.filter(
                    recipe=recipe).values_list('id', flat=True)))
        ingredientrecipes = IngredientRecipe.objects.filter(id__in=ingredients)
        length = len(ingredientrecipes)
        for counter1 in range(length-1):
            amount = ingredientrecipes[counter1].amount
            for counter2 in range(counter1+1, length-1):
                if (ingredientrecipes[counter1].ingredient ==
                        ingredientrecipes[counter2].ingredient):
                    amount += ingredientrecipes[counter2].amount
            ShoppingCart.objects.get_or_create(
                ingredient=ingredientrecipes[counter1].ingredient,
                amount=amount,
                user=request.user
            )
        queryset = ShoppingCart.objects.filter(user=request.user)
        serializer = ShoppingSerializer(
            queryset, many=True, context={'request': request})
        response = HttpResponse(json.dumps(serializer.data),
                                content_type='static/json')
        response['Content-Disposition'
                 ] = "attachment, filename = 'ShoppingCart.json'"
        return response
