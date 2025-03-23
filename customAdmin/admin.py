from typing import Any
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.hashers import check_password
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from customAdmin.GroupAdmin import CustomGroupAdmin

from .models import CustomUser
from .customAdminForm import CustomUserCreationForm


class MyLibraryAdminSite(AdminSite):
    """Custom Admin Site with enhanced UI & role management."""
    
    site_title = _('My Site Admin')
    site_header = _('My Administration')
    index_title = _('Site Administration')

    def each_context(self, request):
        """Customize admin site context to display user info."""
        context = super().each_context(request)
        context['site_title'] = _(str(request.user))
        return context

    def get_app_list(self, request: WSGIRequest) -> list[Any]:
        """Customize the application list in the admin panel."""
        
        app_list = super().get_app_list(request)

        # Log Entry URL
        logentry_admin_url = "/admin/recent_actions/"
        logentry_model = {
            'name': capfirst(_('History')),
            'object_name': 'LogEntry',
            'perms': {'view': True, 'add': False, 'change': False, 'delete': False},
            'admin_url': logentry_admin_url,
            'add_url': None,
        }

        students_model = None
        for app in app_list:
            if app['app_label'] == 'students':
                for i, model in enumerate(app['models']):
                    if model['name'] == 'Students':
                        students_model = model
                        app['models'].pop(i)

        for app in app_list:
            if app['name'] == 'Booking':  # Move Students model to Booking section
                if students_model:
                    app['models'].append(students_model)

        return app_list


class CustomUserAdmin(BaseUserAdmin):
    """Admin panel customization for CustomUser model."""
    
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ('username', 'fullname', 'email', 'c_number', 'w_number', 'image_tag', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('username',)

    def image_tag(self, obj):
        """Display user's avatar in the admin panel."""
        if obj.avatar:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.avatar.url))
        return "No Image"
    image_tag.short_description = 'Image'

    fieldsets = (   
        (None, {'fields': ('email', 'username', 'fullname', 'c_number', 'w_number', 'avatar', 'password',  'address', 'expiry_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'fullname', 'avatar', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
    
    # def get_form(self, request, obj=None, **kwargs):

    #     form = super().get_form(request, obj, **kwargs)

    #     if not request.user.is_superuser and not request.user.groups.filter(name="Admin").exists():
    #         # If the user is not an Admin or Super Admin, remove permission fields
    #         form.base_fields.pop('group', None)
    #         form.base_fields.pop('user_permission', None)

    #     return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Handle pop-up edit view in Django admin."""
        if "_popup=1" in request.GET:
            extra_context = extra_context or {}
            extra_context['is_popup'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# Register Custom Admin Site
# 🔒 Register the restricted Group model in Admin
admin.site.unregister(Group)  # Unregister default Group admin
admin_site = MyLibraryAdminSite()
admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(Group, CustomGroupAdmin)  # Register with restrictions
