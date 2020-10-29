from django.urls  import path

from recipe.views import RecipeView, RecipeDetailView

urlpatterns = [
    path('/category/<int:category_id>', RecipeView.as_view()),
    path('/category/<int:category_id>/item/<int:recipe_id>', RecipeDetailView.as_view()),
]