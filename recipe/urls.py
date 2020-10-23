from django.urls  import path

from recipe.views import ViewRecipe, ViewRecipeDetail

urlpatterns = [
    path('recipe', ViewRecipe.as_view()),
    path('recipe_detail', ViewRecipeDetail.as_view()),
]