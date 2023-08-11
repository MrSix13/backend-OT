# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import api_view
# from rest_framework import status
# from django.http import JsonResponse

# from ..repositories.authentication_repository import AuthenticationRepository


# #Registro de usuarios
# @api_view(['POST'])
# class Register(APIView):
#     @staticmethod
#     def post(request):
#         try:
#             if request.method == 'POST':
#                 email = request.data.get('email')
#                 password = request.data.get('password')
                
#                 if not email or not password:
#                     return JsonResponse({"error":"Email y Password son requeridos"}, status= status.HTTP_400_BAD_REQUEST)
                
#                 try:
#                     user = AuthenticationRepository.register_user(email=email, password = password)
#                     if user is not None:
#                         return JsonResponse({"Mensaje":"Usuario Registrado","username":user.name}, status= status.HTTP_200_OK)
#                     else:
#                         return JsonResponse({"Error":"Usuario no registrado correctamente"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 except AuthenticationRepository.DoesNotExist:
#                     return JsonResponse({"Error": "Email ya existe"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
#             else:
#                 return JsonResponse({"Error":"Method POST is required"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#         except Exception as e:
#             return JsonResponse({"Error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)