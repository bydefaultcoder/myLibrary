from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser 

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
admin_site = MyLibraryAdminSite()


# -------------------------------------------