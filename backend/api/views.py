from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .constants import IS_FAVORITED_VALUES, IS_IN_SHOPING_CART_VALUES
from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, ShopingList,
                     ShopingListRecipe, Tag)
from .paginations import DefaultPagination
from .permissions import IsAuthor
from .serializers import (IngredientListSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          TagSerializer)
from .validations import ValidationResult, validate_query_params

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthor],
        'partial_update': [IsAuthor],
        'destroy': [IsAuthor],
        'favorite': [IsAuthenticated],
    }
    filter_class = RecipeFilter
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeCreateSerializer
        else:
            return RecipeSerializer

    def get_permissions(self):
        try:
            permissions = []
            for permission in self.permission_classes_by_action[self.action]:
                permissions.append(permission())
            return permissions
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def validate_is_favorited(self):
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited and is_favorited not in IS_FAVORITED_VALUES:
            return ValidationResult(
                False,
                'is_favorited',
                'Invalid value. Acceptable "true" and "false"',
            )
        return ValidationResult(True, 'is_favorited', '')

    def validate_is_in_shoping_cart(self):
        is_in_shoping_cart = self.request.query_params.get(
            'is_in_shoping_cart'
        )
        if (
            is_in_shoping_cart
            and is_in_shoping_cart not in IS_IN_SHOPING_CART_VALUES
        ):
            return ValidationResult(
                False,
                'is_in_shoping_cart',
                'Invalid value. Acceptable "true" and "false"',
            )
        return ValidationResult(True, 'is_in_shoping_cart', '')

    @validate_query_params(
        [validate_is_favorited, validate_is_in_shoping_cart]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def add_recipe_in_category(self, queryset_users, curent_user, recipe):
        if queryset_users.filter(pk=curent_user.pk).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': 'the recipe has already been added'},
            )

        shoping_list, shoping_list_created = ShopingList.objects.get_or_create(
            user=curent_user
        )
        ShopingListRecipe.objects.get_or_create(
            recipe=recipe,
            shoping_list=shoping_list
        )
        queryset_users.add(curent_user)
        serializer = RecipeListSerializer(recipe)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def del_recipe_from_category(self, queryset_users, curent_user):
        if not queryset_users.filter(pk=curent_user.pk).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': 'Recipe not added'},
            )
        queryset_users.remove(curent_user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_recipe_category(
            self, request, recipe_pk, related_name_category
    ):
        try:
            recipe = Recipe.objects.get(pk=recipe_pk)
        except Recipe.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': 'the recipe isn\'t exists'},
            )

        category_users = getattr(recipe, related_name_category)
        if request.method == 'GET':
            return self.add_recipe_in_category(
                category_users, request.user, recipe
            )

        else:
            return self.del_recipe_from_category(category_users, request.user)

    @action(detail=True, methods=['get', 'delete'], url_name='favorite')
    def favorite(self, request, pk=None):
        return self.handle_recipe_category(
            request, pk, 'users_chose_as_favorite'
        )

    @action(detail=True, methods=['get', 'delete'], url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        return self.handle_recipe_category(request, pk, 'users_put_in_cart')

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        ingredients = {}
        user = self.request.user
        shoping_list = user.shoping_list
        shoping_list_recipes = shoping_list.list_products.all()
        recipes = [item.recipe for item in shoping_list_recipes]

        for recipe in recipes:
            for ingredient_item in recipe.ingredients.all():
                ingredient_name = ingredient_item.ingredient.name
                ingredient_measurement_unit = (
                    ingredient_item.ingredient.measurement_unit
                )
                if ingredients.get(ingredient_name) is not None:
                    ingredients[ingredient_name][0] += ingredient_item.amount
                else:
                    ingredients[ingredient_name] = [
                        ingredient_item.amount, ingredient_measurement_unit
                    ]

        shoping_list_txt = ''
        for ingredient, value in ingredients.items():
            shoping_list_txt += f'{ingredient} ({value[1]}) - {value[0]} \n'
        return HttpResponse(shoping_list_txt, content_type='text/plain')


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    filter_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    Favorite.objects.all()
