# Generated by Django 3.2.7 on 2022-02-02 20:23

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('measurement_unit', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='api.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Title')),
                ('image', models.ImageField(upload_to='recipes/%Y/%m/%d/', verbose_name='Image')),
                ('text', models.TextField(verbose_name='Description')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Minimal value - 1')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(related_name='ingredients', to='api.IngredientRecipe')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='ShopingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shoping_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shoping list',
                'verbose_name_plural': 'Shoping lists',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=320, null=True, samples=None)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShopingListRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_products', to='api.recipe')),
                ('shoping_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_products', to='api.shopinglist')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='api.Tag'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='users_chose_as_favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Favorite recipes'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='users_put_in_cart',
            field=models.ManyToManyField(blank=True, related_name='cart_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Recipes in cart'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='api.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
            },
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_favorite'),
        ),
    ]
