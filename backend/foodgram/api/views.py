from django.shortcuts import render
from rest_framework import filters, status, views, viewsets


class UsersViewSet(viewsets.ModelViewSet):
    pass


class TagsViewSet(viewsets.ModelViewSet):
    pass


class RecipesViewSet(viewsets.ModelViewSet):
    pass


class IngredientsViewSet(viewsets.ModelViewSet):
    pass


class CartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass
