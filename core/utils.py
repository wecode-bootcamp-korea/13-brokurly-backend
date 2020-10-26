import jwt, json, requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET, ALGORITHM
from user.models import User

def access_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET, algorithm = ALGORITHM)
            user         = User.objects.get(user_id = payload['user_id'])
            request.user = user

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper