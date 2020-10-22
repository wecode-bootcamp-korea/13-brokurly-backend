from django.urls  import path

from recipe.views import RegisterRecipe, ViewRecipeCategory, ViewRecipeDetail

urlpatterns = [
    path('register_recipe', RegisterRecipe.as_view()),
    path('view_recipe_category', ViewRecipeCategory.as_view()),
    path('view_recipe_detail', ViewRecipeDetail.as_view()),
]