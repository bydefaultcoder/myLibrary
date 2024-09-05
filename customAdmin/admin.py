from typing import Any
from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .customAdminForm import CustomUserCreationForm
from .models import CustomUser 
from django.contrib.auth.hashers import check_password
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path
from django.contrib.admin.models import LogEntry
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst
# def custom_dashboard_view(request):
#     return render(request, 'admin/profile.html', {
#         'user': request.user,
#         'site_title': 'User Profile',
#         **admin.site.each_context(request),
#     })


class MyLibraryAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _('My site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('My administration')

    # Text to put at the top of the admin index page.
    index_title = _('Site administration')
    

    def each_context(self, request):
        context = super().each_context(request)
        context['site_title'] = _(str(request.user))
        return context

    
    def get_app_list(self, request: WSGIRequest) -> list[Any]:        # Get the original app list
        app_list = super().get_app_list(request)
        logentry_admin_url = "/admin/recent_actions/"
   

        # Define the LogEntry model entry
        logentry_model = {
            'name': capfirst(_('History')),
            'object_name': 'LogEntry',
            'perms': {
                'add': False,
                'change': False,
                'delete':  False,
                'view': True
            },
            'admin_url': logentry_admin_url,
            'add_url': None,
        }

        # Add this to an existing app (like 'Admin') or create a new app
        # if app['name'] == 'Booking':
        # added = False
        studentsModel = None
        # p = []
        for app in app_list:
            if app['app_label'] == 'students':
              i = 0
              for model in app['models']:
                  if model['name'] == 'Students':
                      studentsModel = model
                      app['models'].pop(i)
                  i = i + 1

        for app in app_list:
            # print(app)
            if app['name'] == 'Booking':  # You can target the existing 'Admin' app
                print("added")
                app['models'].append(studentsModel)
                app['models'].append(logentry_model)
                # added = True
            

        return app_list


        
    def index(self, request, extra_context=None):
        # Use the custom user model to filter actions by the logged-in user
        recent_actions = LogEntry.objects.filter(
            user=request.user,  # request.user will be an instance of CustomUser
            action_time__gte=now() - timedelta(days=7)  # Adjust the time range as needed
        ).select_related('content_type')[:10]  # Limiting to the last 10 actions
    

        extra_context = extra_context or {}
        extra_context['recent_actions'] = recent_actions
        return super().index(request, extra_context=extra_context)

 

    
    
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm  # Use custom form for adding users
    model = CustomUser
    list_display = ('username','fullname', 'email','c_number','w_number','image_tag', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('username',)

    def image_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.avatar.url))

    image_tag.short_description = 'Image'

    fieldsets = (   
        (None, {'fields': ('email', 'username','fullname','c_number','w_number','avatar','password','library_name','address','expiry_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','fullname','avatar', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')  # Enable horizontal filtering for groups and permissions

    # def get_c

    # def save_model(self, request, obj, form, change):
    #     # Only set password if it's being provided (for new users or if password is being changed)
    #     # obj.first_name = form.cleaned_data.get('first_name', obj.first_name)
    #     # obj.last_name = form.cleaned_data.get('last_name', obj.last_name)
    #     if not request.user:
    #         password = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
    #         if password:
    #             obj.set_password(password)
            
    #     super().save_model(request, obj, form, change)

admin_site = MyLibraryAdminSite()

