from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, user_object):
        return Follow.objects.filter(
            user=self.context['request'].user.id, following=user_object.id
        ).exists()

    def get_recipes_count(self, user_object):
        return user_object.recipes.all().count()

    def get_recipes(self, user_object):
        from api.serializers import RecipeListSerializer
        return RecipeListSerializer(
            user_object.recipes.all(), read_only=True, many=True
        ).data


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserRecipeSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
