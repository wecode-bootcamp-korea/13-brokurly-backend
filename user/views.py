import json, re, bcrypt, jwt

from django.views   import View
from django.http    import JsonResponse

from my_settings    import SECRET
from user.models    import User, Gender, ShoppingBasket
from product.models import Product

class SignUp(View): # 회원가입
    def post(self, request):
        data = json.loads(request.body)

        try:
            print("signup start")
            for key in data.keys():
                if data['user_id'] == '' or data['password'] == '' or data['user_name'] == '' or data['phone'] == '' or data['address'] == '':
                    return JsonResponse({'message' : 'NOT_ENTERED_' + str.upper(key)}, status = 400)
            
            print('password')
            password = data['password']
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            User.objects.create(
                user_id           = data['user_id'],
                password          = hashed_pw.decode('utf-8'),
                user_name         = data['user_name'],
                email             = data['email'],
                phone             = data['phone'],
                address           = data['address'],
                gender            = Gender(id = data['gender']),
                date_of_birth     = data['date_of_birth'],
                recommender       = data['recommender'],
                event             = data['event'],
                is_privacy_policy = data['is_privacy_policy'],
                is_sms_agreed     = data['is_sms_agreed'],
                is_email_agreed   = data['is_email_agreed'],
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class CheckID(View): # 아이디 중복확인
    def post(self, request):
        data = json.loads(request.body)

        try:
            if data['user_id'] == '':
                return JsonResponse({'message' : 'NOT_ENTERED_USER_ID'}, status = 400)

            if User.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'USER_ID_DUPLICATED'}, status = 400)
            else:
                return JsonResponse({'message' : 'USER_ID_AVAILABLE'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class CheckEmail(View): # 이메일 중복확인
    def post(self, request):
        data = json.loads(request.body)

        try:
            if data['email'] == '':
                return JsonResponse({'message' : 'NOT_ENTERED_EMAIL'}, status = 400)

            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if p.match(str(data['email'])) == None:
                return JsonResponse({'message':'EMAIL_VALIDATION'}, status = 400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'EMAIL_DUPLICATED'}, status = 400)
            else:
                return JsonResponse({'message' : 'EMAIL_ID_AVAILABLE'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class SignIn(View): # 로그인
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(user_id = data['user_id']).exists():
                user_data = User.objects.get(user_id = data['user_id'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user_data.password.encode('utf-8')) == False:
                    return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
                
                access_token = jwt.encode({'user_id' : data['user_id']}, SECRET, algorithm = 'HS256')

                return JsonResponse({'message' : 'SUCCESS', 'authorization' : access_token.decode('utf-8')}, status = 200)
            else:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)                    
            
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class RegisterShoppingBasket(View): # 장바구니 등록
    def post(self, request):
        data = json.loads(request.body)

        try:
            ShoppingBasket.objects.create(
                quantity = data['quantity'],
                user = User(id = data['user']),
                product = Product(id = data['product']),
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

# class ViewShoppingBasket(View):
#     def get(self, request):
#         data = json.loads(request.body)

#         try:

#         except KeyError as ex:
#             return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)