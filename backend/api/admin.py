from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug',
        'color',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date',)
    fields = (
        'name',
        'author',
        'tags',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ['name', 'author__username', 'tags__name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'measurement_unit')
    fields = ('name', 'measurement_unit')
