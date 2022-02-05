from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(
        format='hexa',
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return (f'{self.ingredient} - {self.amount} '
                f'{self.ingredient.measurement_unit}')


class Recipe(models.Model):
    name = models.CharField('Title', max_length=200)
    image = models.ImageField('Image', upload_to=r'recipes/%Y/%m/%d/')
    text = models.TextField('Description')
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(
        IngredientRecipe,
        related_name='ingredients'
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    users_chose_as_favorite = models.ManyToManyField(
        User,
        verbose_name="Favorite recipes",
        related_name="favorite_recipes",
        blank=True,
    )
    users_put_in_cart = models.ManyToManyField(
        User,
        verbose_name="Recipes in cart",
        related_name="cart_recipes",
        blank=True,
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Minimal value - 1')
        ]
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'),
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class ShopingList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_list'
    )

    class Meta:
        verbose_name = 'Shoping list'
        verbose_name_plural = 'Shoping lists'

    def __str__(self):
        return f'{str(self.user).title()} shoping list'


class ShopingListRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='list_products'
    )
    shoping_list = models.ForeignKey(
        ShopingList,
        on_delete=models.CASCADE,
        related_name='list_products'
    )

    def __str__(self):
        return f'{self.recipe} in {self.shoping_list}'
