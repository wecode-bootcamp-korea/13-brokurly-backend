from django.urls  import path

from recipe.views import RecipeView

urlpatterns = [
    path('/category/<int:category_id>/item/<int:recipe_id>', RecipeView.as_view()),
]