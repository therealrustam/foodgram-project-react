from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartViewSet, CreateUserView, FavoriteViewSet,
                    SubscribeViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

app_name = 'api'
router = DefaultRouter()
router1 = DefaultRouter()
router2 = DefaultRouter()

router.register('users', CreateUserView, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router2.register('subscriptions', SubscribeViewSet, basename='subscriptions')
router1.register('shopping_cart', CartViewSet, basename='shopping_cart')
router1.register('favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:post_id>/', include(router1.urls)),
    path('users/', include(router2.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/download_shopping_cart/', CartViewSet)
]
