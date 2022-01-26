from django.contrib import admin

from .models import (ShopingList, ShopingListRecipe, Tag, Recipe, Ingredient,
                     IngredientRecipe,
                     Favorite)

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(Favorite)
admin.site.register(ShopingList)
admin.site.register(ShopingListRecipe)
