import json
import re
import bcrypt
import jwt
import uuid
import os

from django.views   import View
from django.http    import JsonResponse

from my_settings    import SECRET, ALGORITHM
from user.models    import Order, Review, User, Gender, ShoppingBasket, FrequentlyPurchasedProduct, UserRank, SMS
from product.models import Product
from core.utils     import access_decorator
from twilio.rest    import Client

class SignUpView(View): # 회원가입
    def post(self, request):
        try:
            data = json.loads(request.body)

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
                rank              = UserRank(id = 1),
            )
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except ValueError as ex:
            return JsonResponse({'message' : 'VALUE_ERROR_' + ex.args[0]}, status = 400)

class CheckIdView(View): # 아이디 중복확인
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not data['user_id'] == '':
                if User.objects.filter(user_id = data['user_id']).exists():
                    return JsonResponse({'message' : 'USER_ID_DUPLICATED'}, status = 400)

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            return JsonResponse({'message' : 'NOT_ENTERED_USER_ID'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class CheckEmailView(View): # 이메일 중복확인
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not data['email'] == '':
                email_validation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                if email_validation.match(str(data['email'])) == None:
                    return JsonResponse({'message':'EMAIL_VALIDATION'}, status = 400)

                if User.objects.filter(email = data['email']).exists():
                    return JsonResponse({'message' : 'EMAIL_DUPLICATED'}, status = 400)
                
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            return JsonResponse({'message' : 'NOT_ENTERED_EMAIL'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class SignInView(View): # 로그인
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)                    
            
            user_data = User.objects.get(user_id = data['user_id'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user_data.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
            
            access_token = jwt.encode({'user_id' : data['user_id']}, SECRET, algorithm = ALGORITHM)

            user_dic = {
                'id'            : user_data.id,
                'user_name'     : user_data.user_name,
                'email'         : user_data.email,
                'phone'         : user_data.phone,
                'address'       : user_data.address,
                'date_of_birth' : user_data.date_of_birth,
                'user_rank'     : user_data.rank.name
            }

            return JsonResponse({'message' : 'SUCCESS', 'authorization' : access_token.decode('utf-8'), 'user' : user_dic}, status = 200)
            
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class FindIdView(View): # 회원 아이디 찾기
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(user_name = data['user_name'], email = data['email']).exists():
                return JsonResponse({'message' : 'NOT_EXISTS_USER_NAME_OR_EMAIL'}, status = 400)

            user_id = User.objects.get(user_name = data['user_name'], email = data['email']).user_id

            return JsonResponse({'message' : 'SUCCESS', 'user_id' : user_id}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class FindPasswordView(View):
    def post(self, request): # 비밀번호 찾기 유저 정보 확인
        try:
            data = json.loads(request.body)

            if User.objects.filter(user_id = data['user_id'], email = data['email'], user_name = data['user_name']).exists():
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def patch(self, request): # 새로운 비밀번호로 변경
        try:
            data = json.loads(request.body)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user_password = User.objects.get(user_id = data['user_id']).password

            if bcrypt.checkpw(user_password.encode('utf-8'), hashed_pw):
                return JsonResponse({'message' : 'EQUAL_PASSWORD'}, status = 400)

            user = User.objects.get(user_id = data['user_id'])
            user.password = hashed_pw.decode('utf-8')
            user.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)            

class UserDataView(View): # 회원 정보 조회(메인페이지, 주문하기 등)
    @access_decorator
    def get(self, request):
        try:
            user = request.user

            user_data = {
                'id'            : user.id,
                'user_name'     : user.user_name,
                'email'         : user.email,
                'phone'         : user.phone,
                'address'       : user.address,
                'date_of_birth' : user.date_of_birth,
                'user_rank'     : user.rank.name
            }

            return JsonResponse({'message' : 'SUCCESS', 'user_data' : user_data}, status = 200)
            
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class SendSmsView(View): # 문자 인증 보내기
    def post(self, request):
        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)
            
            sms_num = SMS.objects.order_by('?').first().number
            message = client.messages \
                            .create(
                                body="인증번호 [" + sms_num + "]",
                                to='+8201098825898',
                                from_='+12568264151'
                            )
            
            return JsonResponse({'message' : 'SUCCESS', 'access_number' : sms_num}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class CheckSmsView(View): # 문자 인증 확인
    def post(self, request):
        try:
            data = json.loads(request.body)

            if SMS.objects.filter(number = data['access_number']).exists():
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            
            return JsonResponse({'message' : 'INVALID_NUMBER'}, status = 400)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class ShoppingBasketView(View): # 장바구니
    @access_decorator
    def post(self, request): # 장바구니 등록
        try:
            data = json.loads(request.body)
            user = request.user

            if ShoppingBasket.objects.filter(user=user.id, product=data['product_id']).exists():
                item = ShoppingBasket.objects.get(user=user.id, product=data['product_id'])
                item.quantity += data['quantity']
                item.save()
            else:
                ShoppingBasket.objects.create(
                    quantity = data['quantity'],
                    user     = User(id = user.id),
                    product  = Product(id = data['product_id']),
                )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
    @access_decorator
    def get(self, request): # 장바구니 조회
        try:
            user = request.user

            shopping_list = [{
                    'id'             : item.id,
                    'quantity'       : item.quantity,
                    'product_id'     : item.product_id,
                    'user_id'        : item.user_id,
                    'checked'        : item.checked,
                    'name'           : item.product.name,
                    'price'          : item.product.price,
                    'discount_price' : item.product.price - int(item.product.price * item.product.discount.discount_percent * 0.01),
                    'sold_out'       : item.product.is_sold_out,
                    'sales'          : item.product.sales_count,
                    'image_url'      : item.product.image_url
                } for item in ShoppingBasket.objects.filter(user=user.id)]
                
            return JsonResponse({'message' : 'SUCCESS', 'shopping_list' : shopping_list}, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
    def patch(self, request): # 장바구니 수량 변경
        try: 
            data = json.loads(request.body)

            quantity_change = {
                'plus'  : 1,
                'minus' : -1
            }

            item = ShoppingBasket.objects.get(id = data['shopbasket_id'])

            if (data['increase_or_decrease'] == 'minus') and (item.quantity == 1):
                item.delete()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            item.quantity = item.quantity + (quantity_change[data['increase_or_decrease']])
            item.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
    def delete(self, request): # 장바구니 단일 목록 삭제
        try:
            data = json.loads(request.body) 

            if not ShoppingBasket.objects.filter(id = data['shopbasket_id']).exists():
                return JsonResponse({'message' : 'NOT_EXISTED'}, status = 400)
                
            item = ShoppingBasket.objects.get(id = data['shopbasket_id'])
            item.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class ShoppingBasketCheckView(View):
    @access_decorator
    def patch(self, request): # 장바구니 목록 체크박스 선택/해제
        try:
            data = json.loads(request.body)

            if data['selected'] == 'all':
                basket_list = ShoppingBasket.objects.filter(checked=True) if ShoppingBasket.objects.filter(checked=False).count() == 0 else ShoppingBasket.objects.filter(checked=False)
                for item in basket_list:
                    item.checked = False if item.checked else True
                    item.save()

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            elif data['selected'] == 'single':
                if not ShoppingBasket.objects.filter(id = data['shopbasket_id']).exists():
                    return JsonResponse({'message' : 'NOT_EXISTED'}, status = 400)

                item = ShoppingBasket.objects.get(id = data['shopbasket_id'])
                item.checked = False if item.checked else True
                item.save()

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

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

            elif data['delete'] == 'soldout':
                for item in ShoppingBasket.objects.all():
                    if item.product.is_sold_out:
                        item.delete()
                
            else:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status = 400)

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
class FrequentlyProductView(View): # 늘 사는 것
    @access_decorator
    def post(self, request): # 늘 사는 것 등록
        try:
            data = json.loads(request.body)
            user = request.user
            
            if user.frequently_purchased_product.filter(id = data['product_id']).exists():
                return JsonResponse({'message' : 'ALREADY_BEEN_REGISTERED'}, status = 200)
            else:    
                FrequentlyPurchasedProduct.objects.create(
                    product     = Product(id = data['product_id']),
                    user        = User(id = user.id),
                    description = '',
                    quantity    = 1
                )

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
    
    @access_decorator
    def get(self, request): # 늘 사는 것 조회
        try:
            user = request.user

            product_list = [{
                'id'             : item.id,
                'description'    : item.description,
                'user_id'        : item.user.id,
                'product_id'     : item.product.id,
                'name'           : item.product.name,
                'price'          : item.product.price,
                'discount_price' : item.product.price - int(item.product.price * item.product.discount.discount_percent * 0.01),
                'image_url'      : item.product.image_url,
                'quantity'       : item.quantity
            } for item in FrequentlyPurchasedProduct.objects.filter(user_id = user.id)]

            return JsonResponse({'message' : 'SUCCESS', 'product_list' : product_list}, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
    def delete(self, request): # 늘 사는 것 목록 삭제
        try:
            user = request.user

            FrequentlyPurchasedProduct.objects.filter(user = user.id).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class UserReviewView(View): # 유저의 상품 리뷰
    @access_decorator
    def post(self, request): # 유저의 상품 리뷰 등록
        try: 
            data = json.loads(request.body)
            user = request.user

            contents = data['content'].split('>')
            Review.objects.create(
                title       = data['title'],
                help_count  = 0,
                views_count = 0,
                content     = contents[0],
                user        = User(id = user.id),
                product     = Product(id = data['product_id']),
                image_url   = contents[1] if data['content'].find('>') > -1 else ''
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
        
class ProductReviewView(View):
    def post(self, request, product_id): # 상품의 리뷰 상세보기 클릭 시 조회 수 증가
        try:
            data = json.loads(request.body)

            if not Review.objects.filter(id = data['review_id']).exists():
                return JsonResponse({'message' : 'NOT_EXISTSED_REVIEW'}, status = 400)

            review = Review.objects.get(id = data['review_id'])
            review.views_count += 1
            review.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def get(self, request, product_id): # 상품의 전체리뷰 조회
        try: 
            product    = Product.objects.get(id = product_id)
            offset     = int(request.GET.get('offset'), 0)
            limit      = int(request.GET.get('limit'), 10)

            reviews = Review.objects.order_by('-id').select_related('product', 'user', 'user__rank').filter(product = product.id)
            review_list = [{
                'id'           : item.id,
                'title'        : item.title,
                'create_time'  : item.create_time,
                'help_count'   : item.help_count,
                'views_count'  : item.views_count,
                'content'      : item.content,
                'user_name'    : item.user.user_name,
                'product_id'   : item.product_id,
                'image_url'    : item.image_url,
                'user_rank'    : item.user.rank.name,
                'product_name' : item.product.name,
            } for item in reviews[offset:limit]]

            return JsonResponse({
                'message' : 'SUCCESS', 
                'review_list' : review_list, 
                'total_count'  : reviews.count()
            }, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

class OrderHistoryView(View):
    @access_decorator
    def post(self, request): # 주문내역 등록
        try:
            user = request.user

            number = uuid.uuid4()
            order_num = str(number.int)

            for item in ShoppingBasket.objects.filter(user = user.id, checked = True):
                Order.objects.create(
                    order_number = order_num[:8],
                    price        = item.product.price,
                    product_id   = item.product.id,
                    user_id      = user.id,
                )
                item.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    @access_decorator
    def get(self, request): # 주문내역 조회하기
        try:
            user = request.user

            order_list = [{
                'id'                : item.id,
                'order_number'      : item.order_number,
                'price'             : item.price,
                'create_time'       : item.create_time,
                'product_name'      : item.product.name,
                'product_image_url' : item.product.image_url
            } for item in Order.objects.filter(user = user.id)]

            return JsonResponse({'message' : 'SUCCESS', 'order_list' : list(order_list)}, status = 200)

        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

