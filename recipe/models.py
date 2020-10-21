from django.db import models

class RecipeCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'recipe_categories'
        

class Recipe(models.Model):
    name            = models.CharField(max_length=50)
    writer          = models.CharField(max_length=50)
    image_url       = models.CharField(max_length=200)
    create_time     = models.DateTimeField(auto_now_add=True)
    views_count     = models.IntegerField(default=0)
    content         = models.CharField(max_length=1000)
    recipe_category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipes'