import os
from typing import Iterable
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from dateutil.relativedelta import relativedelta
# Create your models here.
from django.contrib.auth.models import AbstractUser
# from groups
# from django_group_model.models import AbstractGroup
# AbstractGroup
from django.core.validators import MinValueValidator,MaxLengthValidator,MinLengthValidator
from django.db import models
from django.utils import timezone


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
    
    def user_avatar_upload_to(instance, filename):
    # Ensure the user ID is available
        ext = os.path.splitext(filename)[1]  # Get file extension (e.g., .jpg or .png)
        
        # Construct the new filename
        new_filename = f'{instance.username}{ext}'
        
        # Return the full path to the file
        print(new_filename)
        return os.path.join('avatars', new_filename)
    avatar = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True)

    email = models.EmailField(unique=True)
    w_number = models.CharField(max_length=10,validators=[MaxLengthValidator(10),MinLengthValidator(10)],verbose_name="Whatsapp No.")
    c_number = models.CharField(max_length=10,validators=[MaxLengthValidator(10),MinLengthValidator(10)],verbose_name="Calling No.")
    username = models.CharField(blank=False,null=False,max_length=200,unique=True)
    fullname = models.CharField(blank=False,null=False,max_length=200,default="not taken")
    library_name = models.CharField(blank=True,null=True,max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True,null=True)
    # birthdate = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # Add other fields here
    objects = CustomUserManager()
        # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'email']

    def save(self, *args, **kwargs) -> None:
        if not self.pk :
            # self.date_joined = timezone.localdate(self.date_joined)
            self.expiry_date = self.date_joined + relativedelta(months=1)
            # self.expiry_date =  self.date_joined + relativedelta(months=1)
        # else:
        print(self.first_name,self.last_name)


        return super().save( *args, **kwargs)

    def __str__(self):
        return self.username