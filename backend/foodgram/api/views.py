from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (ShopingList, Recipe, Tag, Ingredient, Favorite,
                     ShopingListRecipe)
from .serializers import (RecipeSerializer, RecipeListSerializer,
                          RecipeCreateSerializer, IngredientListSerializer,
                          TagSerializer)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'put', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return RecipeCreateSerializer
        return RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    Favorite.objects.all()


class FavoriteCreateAndDeleteViewSet(views.APIView):

    def get(self, requset, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = Favorite.objects.filter(
            user=self.request.user,
            recipe=recipe
        )
        if not favorite:
            Favorite.objects.create(user=self.request.user, recipe=recipe)
            return Response(
                RecipeListSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': 'The recipe is already in the favorites'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, requset, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = Favorite.objects.filter(
            user=self.request.user,
            recipe=recipe
        )
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
                {'errors': 'There is no recipe in the favorites'},
                status=status.HTTP_400_BAD_REQUEST
        )


class ShopingListCreateAndDeleteViewSet(views.APIView):

    def get(self, requset, id):
        recipe = get_object_or_404(Recipe, id=id)
        shoping_list, shoping_list_created = ShopingList.objects.get_or_create(
            user=self.request.user
        )
        recipe_in_shoping_list, recipe_in_list_created = (
            ShopingListRecipe.objects.get_or_create(
                recipe=recipe,
                shoping_list=shoping_list
            )
        )
        if recipe_in_list_created:
            return Response(
                RecipeListSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': 'The recipe is already in the shoping list'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, requset, id):
        recipe = get_object_or_404(Recipe, id=id)
        shoping_list, shoping_list_created = ShopingList.objects.get_or_create(
            user=self.request.user
        )
        recipe_in_shoping_list = ShopingListRecipe.objects.filter(
            recipe=recipe,
            shoping_list=shoping_list
        )
        if recipe_in_shoping_list:
            recipe_in_shoping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'There is no recipe in the shoping list'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopingListDownloadViewSet(views.APIView):

    def get(self, requset):
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
            shoping_list_txt += f'{ingredient} ({value[1]}) - {value[0]}' + '\n'
        # with open('media/shoping_list.txt', 'w') as file:
        #     for ingredient, value in ingredients.items():
        #         file.write(f'{ingredient} ({value[1]}) - {value[0]}' + '\n')
        return HttpResponse(shoping_list_txt, content_type='text/plain')
