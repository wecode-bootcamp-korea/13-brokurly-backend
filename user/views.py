import json, re, bcrypt, jwt

from django.views   import View
from django.http    import JsonResponse

from my_settings    import SECRET
from user.models    import User, Gender, ShoppingBasket
from product.models import Product, ProductOption

class SignUp(View): # 회원가입
    def post(self, request):
        data = json.loads(request.body)

        try:
            for key in data.keys():
                if data['user_id'] == '' or data['password'] == '' or data['user_name'] == '' or data['phone'] == '' or data['address'] == '':
                    return JsonResponse({'message' : 'NOT_ENTERED_' + str.upper(key)}, status = 400)
            
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

                user_dic = {}
                user_dic['user_name'] = user_data.user_name
                user_dic['address']   = user_data.address
                user_dic['phone']     = user_data.phone
                user_dic['email']     = user_data.email

                return JsonResponse({'message' : 'SUCCESS', 'authorization' : access_token.decode('utf-8'), 'user' : user_dic}, status = 200)
            else:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)                    
            
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class RegisterShoppingBasket(View): # 장바구니 등록
    def post(self, request):
        data = json.loads(request.body)

        #옵션 없는거 예외처리 추가해야됨.
        try:
            ShoppingBasket.objects.create(
                quantity = data['quantity'],
                user     = User(id = data['user_id']),
                product  = Product(id = data['product_id']),
                option   = data['option'],
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class ViewShoppingBasket(View): # 장바구니 표출
    def get(self, request):
        data = json.loads(request.body)

        try:
            shopping_list = ShoppingBasket.objects.filter(user = data['user_id']).values()
            shopping_list = list(shopping_list)

            for item in shopping_list:
                product = Product.objects.filter(id = item['product_id']).get()
                item['name']     = product.name
                item['price']    = product.price
                item['sold_out'] = product.is_sold_out
                item['sales']    = product.sales_rate

                if item['option'] != 0:
                    product_option = ProductOption.objects.filter(product = item['product_id'], id = item['option']).get()
                    item['option_name']     = product_option.name
                    item['option_price']    = product_option.price
                    item['option_sold_out'] = product_option.is_sold_out
                    item['option_sales']    = product_option.sales_limit
            
            return JsonResponse({'message' : 'SUCCESS', 'shopping_list' : shopping_list}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)