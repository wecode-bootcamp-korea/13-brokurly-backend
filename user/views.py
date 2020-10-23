import json, re, bcrypt, jwt

from django.views   import View
from django.http    import JsonResponse

from my_settings    import SECRET
from user.models    import Review, User, Gender, ShoppingBasket, FrequentlyPurchasedProduct
from product.models import Product, ProductOption
from core.utils     import access_decorator

class SignUp(View): # 회원가입
    def post(self, request):
        try:
            data = json.loads(request.body)

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
        try:
            data = json.loads(request.body)

            if data['user_id'] == '':
                return JsonResponse({'message' : 'NOT_ENTERED_USER_ID'}, status = 400)

            if User.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'USER_ID_DUPLICATED'}, status = 400)
            else:
                return JsonResponse({'message' : 'USER_ID_AVAILABLE'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class CheckEmail(View): # 이메일 중복확인
    def post(self, request):
        try:
            data = json.loads(request.body)

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
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class SignIn(View): # 로그인
    def post(self, request):
        try:
            data = json.loads(request.body)

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
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class ShoppingBasketView(View): # 장바구니
    def post(self, request): # 장바구니 등록
        try:
            data = json.loads(request.body)

            ShoppingBasket.objects.create(
                quantity = data['quantity'],
                user     = User(id = data['user_id']),
                product  = Product(id = data['product_id']),
                option   = data['option'],
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
    def get(self, request): # 장바구니 조회
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET, algorithm='HS256')

            shopping_list = ShoppingBasket.objects.filter(user = payload['user_id']).values()
            shopping_list = list(shopping_list)

            for item in shopping_list:
                product = Product.objects.filter(id = item['product_id']).get()
                item['name']      = product.name
                item['price']     = product.price
                item['sold_out']  = product.is_sold_out
                item['sales']     = product.sales_count
                item['image_url'] = product.image_url

                if item['option'] != 0:
                    product_option = ProductOption.objects.filter(product = item['product_id'], id = item['option']).get()
                    item['option_name']     = product_option.name
                    item['option_price']    = product_option.price
                    item['option_sold_out'] = product_option.is_sold_out
                    item['option_sales']    = product_option.sales_limit
                else:
                    item['option_name']     = ''
                    item['option_price']    = product.price
                    item['option_sold_out'] = ''
                    item['option_sales']    = ''
            
            return JsonResponse({'message' : 'SUCCESS', 'shopping_list' : shopping_list}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def put(self, request): # 장바구니 수량 변경
            try:
                data = json.loads(request.body)

                item = ShoppingBasket.objects.filter(id = data['shopbasket_id']).get()

                if data['increase_or_decrease'] == 'plus':
                    item.quantity += 1
                    item.save()
                elif data['increase_or_decrease'] == 'minus':
                    item.quantity -= 1
                    item.save()
                
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            except KeyError as ex:
                return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
            except Exception as ex:
                return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def delete(self, request): # 장바구니 목록 삭제
        try:
            data = json.loads(request.body) 

            if ShoppingBasket.objects.filter(id = data['shopbasket_id']).exists():
                item = ShoppingBasket.objects.filter(id = data['shopbasket_id']).get()
                item.delete()
            else:
                return JsonResponse({'message' : 'NOT_EXISTED'}, status = 400)

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class ShoppingBasketCheckView(View): 
    def put(self, request): # 장바구니 목록 선택/해제
        try:
            data = json.loads(request.body)

            if ShoppingBasket.objects.filter(id = data['shopbasket_id']).exists():
                item = ShoppingBasket.objects.filter(id = data['shopbasket_id']).get()
                item.checked = False if item.checked else True
                item.save()
            else:
                return JsonResponse({'message' : 'NOT_EXISTED'}, status = 400)

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class FrequentlyProductView(View): # 늘 사는 것
    def post(self, request): # 늘 사는 것 등록
        try:
            data = json.loads(request.body)

            if FrequentlyPurchasedProduct.objects.filter(user = data['user_id'], product = data['product_id']).exists():
                return JsonResponse({'message' : 'ALREADY_BEEN_REGISTERED'}, status = 400)
            else:    
                FrequentlyPurchasedProduct.objects.create(
                    product     = Product(id = data['product_id']),
                    user        = User(id = data['user_id']),
                    description = data['description'],
                )

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
    def get(self, request): # 늘 사는 것 조회
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET, algorithm='HS256')
            user = User.objects.filter(user_id = payload['user_id']).get().id

            product_list = FrequentlyPurchasedProduct.objects.filter(user_id = user).values()
            product_list = list(product_list)

            for item in product_list:
                product = Product.objects.filter(id = item['product_id']).get()
                item['name']  = product.name
                item['price'] = product.price
            
            return JsonResponse({'message' : 'SUCCESS', 'product_list' : product_list}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def delete(self, request): # 늘 사는 것 목록 삭제
        try:
            data = json.loads(request.body)

            item = FrequentlyPurchasedProduct.objects.filter(id = data['product_id']).get()
            item.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class ProductReview(View): # 상품 리뷰
    def post(self, request): # 상품 리뷰 등록
        try:
            data = json.loads(request.body)

            Review.objects.create(
                name        = data['name'],
                help_count  = 0,
                views_count = 0,
                content     = data['content'],
                user        = User(id = data['user_id']),
                product     = Product(id = data['product_id']),
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
        
    
    # def get(self, request): # 상품 리뷰 조회
    #     token = json.loads(request.headers)
    #     payload = jwt.decode(token, SECRET, algorithm='HS256')
        