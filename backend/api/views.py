"""
Создание view классов обработки запросов.
"""
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Subscribe, Tag)
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response
from users.models import User

from .filters import RecipeFilters
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RegistrationSerializer, SubscribeSerializer,
                          SubscriptionSerializer, TagSerializer)


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

    def list(self, request, *args, **kwargs):
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

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(status=201)

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
    filter_class = RecipeFilters
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]

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

    def create(self, request, *args, **kwargs):
        recipes_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipes_id)
        Cart.objects.create(
            user=request.user, recipes=recipe)
        return Response(status=201)

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

    def create(self, request, *args, **kwargs):
        recipes_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipes_id)
        Favorite.objects.create(
            user=request.user, recipes=recipe)
        return Response(status=201)

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


class DownloadCart(viewsets.ModelViewSet):
    """
    Сохранение файла списка покупок.
    """
    permission_classes = [permissions.IsAuthenticated]

    @ staticmethod
    def canvas_method(dictionary):
        """
        Метод сохранения списка покупок в формате PDF.
        """
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename = "shopping_cart.pdf"'
        begin_position_x, begin_position_y = 40, 650
        sheet = canvas.Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans',
                                       'media/FreeSans.ttf'))
        sheet.setFont('FreeSans', 50)
        sheet.setTitle('Список покупок')
        sheet.drawString(begin_position_x,
                         begin_position_y+40, 'Список покупок: ')
        sheet.setFont('FreeSans', 24)
        for number, item in enumerate(dictionary, start=1):
            if begin_position_y < 100:
                begin_position_y = 700
                sheet.showPage()
                sheet.setFont('FreeSans', 24)
            sheet.drawString(
                begin_position_x,
                begin_position_y,
                f'{number}.  {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f' {item["ingredient__measurement_unit"]}'
            )
            begin_position_y -= 30
        sheet.showPage()
        sheet.save()
        return response

    def list(self, request):
        """
        Метод создания списка покупок.
        """
        result = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))
        return self.canvas_method(result)
