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
# from booking.views import get_seats,get_seat_available_timing,get_mothlyplans_by_user
# from customAdmin.views import display_profile, recent_actions
# from customAdmin.views import CustomUserDetailView
# from customAdmin.admin import admin_site


# from django.conf.urls.static import static
# from django.conf import settings 
from .views import dashboard,get_booking,get_trans
from booking.views import get_lib,get_seat,get_plan,create_lib
from students.views import get_student

homeUrls = [
    path('dashboard', view= dashboard ,name='dash' ),
    path('lib', view= get_lib ,name='lib'),
    path('create-lib', view= create_lib ,name='create_lib'),
    path('seat', view= get_seat ,name='seat'),
    path('student', view= get_student ,name='student'),
    path('plan', view= get_plan ,name='plan'),
    path('booking', view= get_booking ,name='booking'),
    path('trans', view= get_trans ,name='trans')
]
