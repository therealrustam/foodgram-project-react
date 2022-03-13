from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (CartViewSet, FavoriteViewSet, IngredientsViewSet,
                    RecipesViewSet, TagsViewSet, UsersViewSet)

app_name = 'api'
router = DefaultRouter()
router1 = DefaultRouter()

router.register('users', UsersViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)
router.register('ingredients', IngredientsViewSet)
router1.register('shopping_cart', CartViewSet)
router1.register('favorite', FavoriteViewSet)

urlpatterns = [
    path('/', include(router.urls)),
    path('recipes/<int:post_id>/', include(router1.urls)),
]
