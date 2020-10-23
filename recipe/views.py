import json

from django.views import View
from django.http import JsonResponse

from recipe.models import Recipe, RecipeCategory

class ViewRecipe(View): # 레시피
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
        data = json.loads(request.body)

        try:
            if data['category_id'] == '':
                recipe_list = Recipe.objects.values('name', 'image_url')
            else:
                recipe_list = Recipe.objects.filter(recipe_category = data['category_id']).values('name', 'image_url')

            return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : list(recipe_list)}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class ViewRecipeDetail(View): # 레시피 상세정보 조회
    def get(self, request):
        data = json.loads(request.body)

        try:
            if data['id'] == '':
                return JsonResponse({'message' : 'INVALID_ID'}, status = 200)
            else:
                recipe = Recipe.objects.filter(id = data['id']).get()
                recipe.views_count += 1
                recipe.save()

                recipe_list = Recipe.objects.filter(id = data['id']).values()

                return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : list(recipe_list)}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)


