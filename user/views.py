import json, re, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET
from user.models  import User

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
                is_gender         = data['is_gender'],
                date_of_birth     = data['date_of_birth'],
                is_add_input      = data['is_add_input'],
                input_description = data['input_description'],
                is_privacy_policy = data['is_privacy_policy'],
                is_sms            = data['is_sms'],
                is_email          = data['is_email'],
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

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
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

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
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

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
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)