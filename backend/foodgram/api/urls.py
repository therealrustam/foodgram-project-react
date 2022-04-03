"""
Создание маршрутизаторов API проекта Foodgram.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (CartViewSet, CreateUserView, FavoriteViewSet,
                    IngredientViewSet, RecipeViewSet, SubscribeViewSet,
                    TagViewSet, DownloadViewSet)

app_name = 'api'
router = DefaultRouter()
router1 = SimpleRouter(trailing_slash=False)


router.register('users', CreateUserView, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes/(?P<recipes_id>\d+)/shopping_cart',
                CartViewSet, basename='shopping_cart')
router.register(r'recipes/(?P<recipes_id>\d+)/favorite',
                FavoriteViewSet, basename='favorite')
router.register(r'users/(?P<users_id>\d+)/subscribe',
                SubscribeViewSet, basename='subscribe')
router.register(r'recipes/(?P<recipes_id>\d+)/favorite',
                FavoriteViewSet, basename='favorite')
router.register(r'users/(?P<users_id>\d+)/subscribe',
                SubscribeViewSet, basename='subscribe')
router1.register(r'recipes/download_shopping_cart',
                 DownloadViewSet, basename='download')
router1.register(r'users/subscriptions',
                 SubscribeViewSet, basename='subscriptions')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(router1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
