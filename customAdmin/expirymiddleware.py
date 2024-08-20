from django.shortcuts import redirect
from datetime import date
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages

from .models import CustomUser
class CheckUserExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        if not request.user.is_authenticated:
            print("not login")
            return self.get_response(request)
        
        today_time = timezone.now().time()
        print("middleware is called")
        userObj = CustomUser.objects.get(pk=request.user.pk)
        # print(userObj.expiry_date )
        if  userObj.expiry_date:
            db_time = userObj.expiry_date.time()
            if today_time < db_time:
                print("user not expired")
            else :
                print("user expired")
                messages.error(request, "Your account has expired.")
                logout(request)
        response = self.get_response(request)
        return response