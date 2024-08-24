from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .customAdminForm import CustomUserCreationForm
from .models import CustomUser 
from django.contrib.auth.hashers import check_password
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
        # self.
        return context

    def get_app_list(self, request):
        """
        Return a custom ordered list of apps and their models.
        """
        # Get the default app list
        app_list = super().get_app_list(request)

        # Define the custom order of apps (by name)
        custom_app_order = ['Authentication and Authorization', 'Booking', 'Customadmin']

        # Define the custom order of models for each app
        custom_model_order = {
            'Authentication and Authorization': ['Groups', 'SecondModel'],
            'Customadmin': ['Users'],
            'Booking': ['Locations','Seats','Students','Bookings', 'Paymentss'],
        }

        # Sort the app list based on the custom app order
        app_list = sorted(app_list, key=lambda x: custom_app_order.index(x['name']) if x['name'] in custom_app_order else len(custom_app_order))

        # Sort models within each app based on custom model order
        for app in app_list:
            app_name = app['name']
            if app_name in custom_model_order:
                # Sort models within this app based on custom model order
                app['models'] = sorted(app['models'], key=lambda x: custom_model_order[app_name].index(x['object_name']) if x['object_name'] in custom_model_order[app_name] else len(custom_model_order[app_name]))

        return app_list
    
    
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm  # Use custom form for adding users
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('email', 'username','password','library_name','library_address','expiry_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')  # Enable horizontal filtering for groups and permissions

    

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

