from django.urls  import path

from recipe.views import RecipeView

urlpatterns = [
    path('/item', RecipeView.as_view()),
]