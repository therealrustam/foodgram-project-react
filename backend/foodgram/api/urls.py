from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartViewSet, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet, CreateUserView)

app_name = 'api'
router = DefaultRouter()
router1 = DefaultRouter()

router.register('users', CreateUserView, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router1.register('shopping_cart', CartViewSet, basename='shopping_cart')
router1.register('favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:post_id>/', include(router1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
