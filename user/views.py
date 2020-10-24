import json, re, bcrypt, jwt

from django.views   import View
from django.http    import JsonResponse

from my_settings    import SECRET
from user.models    import Review, User, Gender, ShoppingBasket, FrequentlyPurchasedProduct, UserRank
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
    @access_decorator
    def post(self, request): # 장바구니 등록
        try: ########### 같은 상품 등록 시 예외처리 ###################
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
    
    @access_decorator
    def get(self, request): # 장바구니 조회
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET, algorithm='HS256')
            userid = User.objects.filter(user_id = payload['user_id']).get().id

            shopping_list = list(ShoppingBasket.objects.filter(user = userid).values())

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

    @access_decorator
    def put(self, request): # 장바구니 수량 변경
            try: 
                data = json.loads(request.body)

                item = ShoppingBasket.objects.filter(id = data['shopbasket_id']).get()

                if data['increase_or_decrease'] == 'plus':
                    item.quantity += 1
                    item.save()
                elif data['increase_or_decrease'] == 'minus':
                    if item.quantity == 1:
                        item.delete()
                    else:
                        item.quantity -= 1
                        item.save()
                
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            except KeyError as ex:
                return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
            except Exception as ex:
                return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
    def delete(self, request): # 장바구니 목록 삭제( X 표시 클릭 시)
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
    @access_decorator
    def put(self, request): # 장바구니 목록 체크박스 선택/해제
        try:
            data = json.loads(request.body)

            if data['selected'] == 'all':
                basket_list = ShoppingBasket.objects.filter(checked=True) if ShoppingBasket.objects.filter(checked=False).count() == 0 else ShoppingBasket.objects.filter(checked=False)
                for item in basket_list:
                    item.checked = False if item.checked else True
                    item.save()

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            elif data['selected'] == 'single':
                if ShoppingBasket.objects.filter(id = data['shopbasket_id']).exists():
                    item = ShoppingBasket.objects.filter(id = data['shopbasket_id']).get()
                    item.checked = False if item.checked else True
                    item.save()

                    return JsonResponse({'message' : 'SUCCESS'}, status = 200)
                else:
                    return JsonResponse({'message' : 'NOT_EXISTED'}, status = 400)

            else:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
    @access_decorator
    def delete(self, request): # 장바구니 선택 상품 or 품절 상품 삭제
        try:
            data = json.loads(request.body)

            if data['delete'] == 'selected':
                for item in ShoppingBasket.objects.filter(checked=True):
                    item.delete()

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            
            elif data['delete'] == 'soldout':
                shopping_list = list(ShoppingBasket.objects.values())

                for item in shopping_list:
                    product = Product.objects.filter(id = item['product_id']).get()

                    if item['option'] != 0:
                        product_option = ProductOption.objects.filter(product = item['product_id'], id = item['option']).get()
                        if product_option.is_sold_out:
                            item.delete()
                    else:
                        if product.is_sold_out:
                            item.delete()
                
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            
            else:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
class FrequentlyProductView(View): # 늘 사는 것
    @access_decorator
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
    
    @access_decorator
    def get(self, request): # 늘 사는 것 조회
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET, algorithm='HS256')
            user = User.objects.filter(user_id = payload['user_id']).get().id

            product_list = list(FrequentlyPurchasedProduct.objects.filter(user_id = user).values())

            for item in product_list:
                product = Product.objects.filter(id = item['product_id']).get()
                item['name']  = product.name
                item['price'] = product.price
            
            return JsonResponse({'message' : 'SUCCESS', 'product_list' : product_list}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
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

class UserReview(View): # 유저의 상품 리뷰
    @access_decorator
    def post(self, request): # 유저의 상품 리뷰 등록
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
        
class ProductReview(View):
    def get(self, request): # 상품의 전체리뷰 조회
        try: 
            product_id = request.GET.get('product_item')
            product = Product.objects.filter(id = product_id).get()

            review_list = Review.objects.filter(product = product.id).values()
            review_list = list(review_list)

            for item in review_list:
                rank = UserRank.objects.filter(user = item['user_id']).get()
                item['user_rank']    = rank.name
                item['product_name'] = product.name

                if ProductOption.objects.filter(product=product.id).exists():
                    product_option = ProductOption.objects.filter(product = product.id, id = item['option']).get()
                    item['product_option_name'] = product_option.name
                else:
                    item['product_option_name'] = ''
                
            return JsonResponse({'message' : 'SUCCESS', 'review_list' : review_list}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)