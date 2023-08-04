# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email requerido')
#         email = self.normalize_email(email)
        
#         username = extra_fields['username']
#         if not username:
#             raise ValueError('Username requerido')
        
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
    

# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=100, unique=True)
#     name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, unique=True)
#     is_active = models.BooleanField(default=True)
    
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']
    
#     def __str__(self):
#         return self.name
