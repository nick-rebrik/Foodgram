from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, \
    ShopingListRecipe, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, ingredient_object):
        return ingredient_object.ingredient.id

    def get_name(self, ingredient_object):
        return ingredient_object.ingredient.name

    def get_measurement_unit(self, ingredient_object):
        return ingredient_object.ingredient.measurement_unit


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    from users.serializers import UserRecipeSerializer
    author = UserRecipeSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, recipe_object):
        return Favorite.objects.filter(
            user=self.context['request'].user.id,
            recipe=recipe_object
        ).exists()

    def get_is_in_shopping_cart(self, recipe_object):
        return ShopingListRecipe.objects.filter(
            recipe=recipe_object
        ).exists()


class RecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients_ = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        for item in ingredients_:
            ingredient, created = IngredientRecipe.objects.get_or_create(
                ingredient_id=item['id'],
                amount=item['amount']
            )
            recipe.ingredients.add(ingredient)
        recipe.tags.add(*tags)
        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients_ = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().update(instance, validated_data)
        for item in ingredients_:
            ingredient, created = IngredientRecipe.objects.get_or_create(
                ingredient_id=item['id'],
                amount=item['amount']
            )
            recipe.ingredients.add(ingredient)
        recipe.tags.add(*tags)
        return recipe


