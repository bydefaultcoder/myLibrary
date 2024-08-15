from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
from django.contrib.auth.models import AbstractUser
# from groups
# from django_group_model.models import AbstractGroup
# AbstractGroup
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(blank=False,null=False,max_length=200,unique=True)
    library_name = models.CharField(blank=False,null=False,max_length=200,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # birthdate = models.DateField(null=True, blank=True)
    library_address = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # Add other fields here

    objects = CustomUserManager()

        # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'email']

    def __str__(self):
        return self.username
    
# class 