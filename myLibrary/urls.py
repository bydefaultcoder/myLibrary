"""
URL configuration for myLibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path, include
from booking.views import get_seats_by_location,get_seat_available_timing,get_mothlyplans_by_user
from customAdmin.views import display_profile, recent_actions
# from customAdmin.views import CustomUserDetailView
from customAdmin.admin import admin_site


from django.conf.urls.static import static
from django.conf import settings 
from .views import homepage
urlpatterns = [
    # path('grappelli/', include('grappelli.urls'))
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    
    path('admin/api-booking/get_timming_by_seat/', get_seat_available_timing, name='get_timming_by_seat'),
    # path('admin/api-booking/get_mothlyplans_by_user/', get_mothlyplans_by_user, name='get_mothlyplans_by_user'),
    # path('admin/user-profile/', CustomUserDetailView.as_view(),name="user_profile"),
    path('admin/user-profile/', display_profile,name="user_profile"),
    path('admin/recent_actions/', recent_actions, name='recent_actions'),
    path('admin/', admin_site.urls),
    path('api/students/', include('students.urls')),
    path('api/get_seats_by_location/', get_seats_by_location, name='get_seats_by_location_w_date'),
    path('', homepage),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_DIR)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
