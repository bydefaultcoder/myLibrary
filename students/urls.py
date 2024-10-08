from django.urls import path
from .views import RegisterAPIView, LoginAPIView
from .library.views import all_libraries
# from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('libraries', all_libraries, name='get_lib'),
]
