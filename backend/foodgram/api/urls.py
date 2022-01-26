from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, ShopingListCreateAndDeleteViewSet,
                    RecipeViewSet, FavoriteCreateAndDeleteViewSet,
                    IngredientViewSet, ShopingListDownloadViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'recipes/<int:id>/favorite/',
        FavoriteCreateAndDeleteViewSet.as_view()
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShopingListCreateAndDeleteViewSet.as_view()
    ),
    path(
        'recipes/download_shopping_cart/',
        ShopingListDownloadViewSet.as_view()
    ),
    path('', include(router.urls))
]
