from django.urls  import path

from recipe.views import RecipeView, RecipeDetailView

urlpatterns = [
    path('recipe', RecipeView.as_view()),
    path('recipe_detail', RecipeDetailView.as_view()),
]