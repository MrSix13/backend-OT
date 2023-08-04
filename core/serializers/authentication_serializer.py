from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name","email", "password"]
        extra_kwargs = {"password":{'write_only':True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        
        #Datos que tendra el token a futuro
        token['email'] = user.email
        token['name']  = user.name
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = CustomUserSerializer(self.user)
        data['email'] = serializer.data.get('email')
        data['name']  = serializer.data.get('name')
        return data
    

class RegisterView(CreateAPIView):
    serializer_class = CustomUserSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer