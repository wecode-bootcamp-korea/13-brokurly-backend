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
                recipe_category = data['recipe_category']
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

    def get(self, request): # 레시피 카테고리별 조회
        try:
            category_id = request.GET.get('category_id')
            recipe_id   = request.GET.get('id')

            if category_id == '0':
                recipe_list = Recipe.objects.order_by('?').values()

            recipe_list = [{
                'id'          : item.id,
                'name'        : item.name,
                'writer'      : item.writer,
                'image_url'   : item.image_url,
                'create_time' : item.create_time,
                'views_count' : item.views_count,
                'content'     : item.content,
            } for item in Recipe.objects.get(recipe_category = 1, id = recipe_id)]

            return JsonResponse({'message' : 'SUCCESS', 'recipe_list' : recipe_list}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)