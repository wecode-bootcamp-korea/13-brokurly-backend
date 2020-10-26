import json

from django.views import View
from django.http import JsonResponse

from recipe.models import Recipe, RecipeCategory

class RecipeView(View): # 레시피
    def post(self, request): # 레시피 등록
        data = json.loads(request.body)
        
        try:
            Recipe.objects.create(
                name            = data['name'],
                writer          = data['writer'],
                image_url       = data['image_url'],
                content         = data['content'],
                recipe_category = RecipeCategory(id = data['recipe_category'])
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

    def get(self, request): # 레시피 카테고리별 조회
        try:
            category_id = request.GET.get('category_id')

            if category_id == '0':
                recipe_list = Recipe.objects.values('id', 'recipe_category_id', 'name', 'image_url')
            else:
                recipe_list = Recipe.objects.filter(recipe_category = category_id).values('id', 'recipe_category_id', 'name', 'image_url')

            return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : list(recipe_list)}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class RecipeDetailView(View): # 레시피 상세정보 조회
    def get(self, request):
        try:
            recipe_id = request.GET.get('recipe_id')

            if recipe_id == '':
                return JsonResponse({'message' : 'INVALID_ID'}, status = 200)
            else:
                recipe = Recipe.objects.filter(id = recipe_id).get()
                recipe.views_count += 1
                recipe.save()

                recipe_list = Recipe.objects.filter(id = recipe_id).values()

                return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : list(recipe_list)}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)


