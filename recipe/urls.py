from django.urls  import path

from recipe.views import RecipeView, RecipeDetailView

urlpatterns = [
    path('/category', RecipeView.as_view()),
    path('/detail', RecipeDetailView.as_view()),
]