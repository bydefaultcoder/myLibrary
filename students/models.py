import os
from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone as tz
from django.core.validators import MinValueValidator,MaxLengthValidator,MinLengthValidator
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from customAdmin.models import CustomUser
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import AbstractUser


class StudentManager(BaseUserManager):
    def create_user(self, phone_no, password=None, **extra_fields):
        if not phone_no:
            raise ValueError('The phone_no field must be set')
        phone_no = phone_no
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
# Create your models here.
class Student(CustomUser):
    objects = StudentManager()
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('alloted', 'Alloted'),
        ('suspended', 'Suspended'),
    ]
    def user_avatar_upload_to(instance, filename):
    # Ensure the user ID is available
        user_id = instance.pk
        ext = os.path.splitext(filename)[1]  # Get file extension (e.g., .jpg or .png)
        # Construct the new filename
        new_filename = f'{user_id}{ext}'
        # Return the full path to the file
        print(new_filename)
        return os.path.join('student/avatars', new_filename)
    username = None
    groups = None
    user_permissions = None
    is_staff = None  # Remove this if students don't need staff access
    is_superuser = None  # Remove this if students don't need superuser access
    # customuser_ptr = None
    # last_login = None  # Remove this if you don't need to track last login
    # email = models.EmailField()

    date_of_birth = models.DateField(null=True,blank=True)
    stu_no = models.PositiveIntegerField(blank=True,null=True,editable=False)
    # avatar = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True)
    phone_no = models.CharField(max_length=10,validators=[MaxLengthValidator(10),MinLengthValidator(10)])
    # address = models.TextField(null=True,blank=True)
    # date_joined =  models.DateField(auto_now=True)
    adhar_no = models.CharField(max_length=12, unique=True,validators=[MaxLengthValidator(12),MinLengthValidator(12)],blank=True)
    # is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enrolled',editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,default=1, null=True, blank=True,editable=False,related_name="students")
    REQUIRED_FIELDS = ['phone_no', 'first_name', 'last_name',]
    USERNAME_FIELD = 'phone_no'

    class Meta:
        verbose_name = "Student"          # Singular form
        verbose_name_plural = "Students"  # Plural form

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.status})"
    def getfullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Check if the status has changed
        print(self.is_staff,self.is_superuser,"hellossssssssssssssssssssssss")
        self.first_name
        if self.pk:
           if self.password and self.created_by.pk==1:
                self.password = make_password(self.password)  # Set your default password here
           else:
                self.password = make_password(f"{self.phone_no}@{self.last_name}")  # Set your default password here
        else:        
           self.stu_no = Student.objects.filter(created_by=self.created_by).count()+ 1
        if self.avatar:
            self.avatar.name = self.avatar.name.replace('None',f'{self.stu_no}') 

        super().save(*args, **kwargs)
