# from django.contrib.auth import authenticate, get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.db import IntegrityError

# User = get_user_model()

# class AuthenticationRepository:
#     @staticmethod
#     def register_user(email, password):
#         try:
#             user = User.objects.create_user(email=email, password=password)
#             return user
#         except IntegrityError:
#             return None
    
#     @staticmethod
#     def authenticate_user(email, password):
#         user = authenticate(email = email, password = password)
#         return user
    
#     @staticmethod
#     def reset_password_request(email):
#         try:
#             user  = User.objects.get(email = email)
#             token = default_token_generator.make_token(user)
#             uid   = urlsafe_base64_encode(force_bytes(user.pk))
#             return uid, token
#         except User.DoesNotExist:
#             return None, None
        
#     @staticmethod
#     def reset_password_confirm(uid, token, new_password):
#         try:
#             uid = force_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(pk=uid)
#             if default_token_generator.check_token(user,token):
#                 user.set.password(new_password)
#                 user.save()
#                 return True
#             else:
#                 return False
#         except(User.DoesNotExist, ValueError, TypeError):
#             return False