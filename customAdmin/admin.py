from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .customAdminForm import CustomUserCreationForm
from .models import CustomUser 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class MyLibraryAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _('My site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('My administration')

    # Text to put at the top of the admin index page.
    index_title = _('Site administration')

    def each_context(self, request):
        context = super().each_context(request)
        context['site_title'] = str(request.user)
        context['site_header'] = str(request.user)
        return context
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm

    # Display these fields in the admin panel
    list_display = ('email', 'username','first_name', 'last_name', 'is_staff', 'is_superuser')

    # Define fieldsets for displaying and editing the user model
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),  # Added permissions field
    )

    # Fields to use when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')  # Enable horizontal filtering for groups and permissions

    def save_model(self, request, obj, form, change):
        # Only set password if it's being provided (for new users or if password is being changed)
        password = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        super().save_model(request, obj, form, change)


admin_site = MyLibraryAdminSite()