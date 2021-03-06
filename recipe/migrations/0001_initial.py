# Generated by Django 3.1.2 on 2020-10-29 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'recipe_categories',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('writer', models.CharField(max_length=50)),
                ('image_url', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('views_count', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=1000)),
                ('recipe_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipecategory')),
            ],
            options={
                'db_table': 'recipes',
            },
        ),
    ]
