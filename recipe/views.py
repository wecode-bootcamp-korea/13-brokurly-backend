import json

from django.views import View
from django.http import JsonResponse

from recipe.models import Recipe, RecipeCategory

class RecipeView(View): # 레시피
    def post(self, request): # 레시피 등록
        try:
            data = json.loads(request.body)

            Recipe.objects.create(
                name            = data['name'],
                writer          = data['writer'],
                image_url       = data['image_url'],
                content         = data['content'],
                recipe_category = data['recipe_category']
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

    def get(self, request, category_id): # 레시피 카테고리별 조회
        try:
            recipe = Recipe.objects.filter(recipe_category = category_id) if category_id != 0 else Recipe.objects.order_by('?')

            recipe_list = [{
                'id'          : item.id,
                'name'        : item.name,
                'image_url'   : item.image_url,
                'category_id' : item.recipe_category.id
            } for item in recipe]

            return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : recipe_list}, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class RecipeDetailView(View):
    def get(self, request, category_id, recipe_id):
        try:
            recipe_list = [{
                    'id'          : item.id,
                    'name'        : item.name,
                    'image_url'   : item.image_url,
                    'writer'      : item.writer,
                    'create_time' : item.create_time,
                    'views_count' : item.views_count,
                    'content'     : item.content,
                    'category_id' : item.recipe_category.id
                } for item in Recipe.objects.filter(recipe_category = category_id, id = recipe_id)]
            
            return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : recipe_list}, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
        
