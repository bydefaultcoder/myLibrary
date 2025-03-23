import os
from django.contrib.auth.models import Group, Permission,BaseUserManager, PermissionsMixin
from django.db.models.signals import post_migrate
from django.db import models
# from django.contrib.auth.models import  Group
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied

# Define User Roles
ROLES = ["Super Admin", "Admin", "Vendor", "Vendor Staff", "Student"]

student_per = ["add_booking","view_booking","view_seat","view_monthlyplan"]

vender_staff_per = ["add_monthlyplan","view_monthlyplan",
                    "add_booking","change_booking","view_booking",
                    "add_seat","change_seat","view_seat",
                    "view_payment",
                    "add_location","change_location","view_location","change_monthlyplan",
                    "add_student","change_student","view_student",
                    "view_bookingpayment",
                    ]
vender_per = ["delete_seat",
              "delete_monthlyplan","delete_booking",
              "delete_location","delete_student","add_payment"] + vender_staff_per
admin_per = ["change_customuser","delete_customuser","view_customuser","add_customuser"] + vender_per
super_admin_per = ["change_payment","delete_payment","add_bookingpayment","change_bookingpayment","delete_bookingpayment"]+admin_per

ROLE_PERMISSIONS = {
    "Super Admin": super_admin_per,
    "Admin":admin_per,
    "Vendor":vender_per,
    "Vendor Staff": vender_staff_per,
    "Student": student_per,
}

@receiver(post_migrate)
def create_roles_and_assign_permissions(sender, **kwargs):
    """Create predefined roles and assign permissions after migration."""
    user_content_type = ContentType.objects.get_for_model(CustomUser)

    for role, permissions in ROLE_PERMISSIONS.items():
        group, created = Group.objects.get_or_create(name=role)

        for perm_code in permissions:
            permission, _ = Permission.objects.get_or_create(codename=perm_code, content_type=user_content_type)
            group.permissions.add(permission)

        print(f"✅ {role} role created with permissions: {permissions}")
        
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,role="Student", **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        group, created = Group.objects.get_or_create(name=role)
        user.save(using=self._db)
        user.groups.add(group)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email,password, role="Super Admin",**extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):  
    def user_avatar_upload_to(instance, filename):
        ext = os.path.splitext(filename)[1]  # Get file extension (e.g., .jpg or .png)
        new_filename = f'{instance.username}{ext}'
        return os.path.join('avatars', new_filename)
    
    avatar = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True)
    email = models.EmailField(unique=True)
    w_number = models.CharField(max_length=10, validators=[MaxLengthValidator(10), MinLengthValidator(10)], verbose_name="Whatsapp No.")
    c_number = models.CharField(max_length=10, validators=[MaxLengthValidator(10), MinLengthValidator(10)], verbose_name="Calling No.")
    username = models.CharField(blank=False, null=False, max_length=200, unique=True)
    # role = models.CharField(blank=False, null=False, max_length=200, unique=True)
    fullname = models.CharField(blank=False, null=False, max_length=200, default="not taken")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)
    address = models.TextField(max_length=500, blank=True)
    
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['email']
    
    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.expiry_date = self.date_joined + relativedelta(months=1)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

# Signal to create groups after migration
@receiver(post_migrate)
def create_roles(sender, **kwargs):
    for role in ROLES:
        Group.objects.get_or_create(name=role)
    print("Roles created successfully!")

# Utility function to check user roles
def has_role(user, role_name):
    return user.groups.filter(name=role_name).exists()



