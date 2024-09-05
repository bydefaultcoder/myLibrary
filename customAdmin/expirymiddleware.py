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
        # print(request.path)
        if not request.user.is_authenticated:
            # print("not login")
            return self.get_response(request)
        # print("middleware is called")
        userObj = CustomUser.objects.get(pk=request.user.pk)
        # print(userObj.expiry_date )
        if  userObj.expiry_date:
            # db_time = userObj.expiry_date.date()
            # print(today_time,db_time)
            # print(request.user.is_superuser)
            print(userObj.expiry_date.date(),timezone.now().date())
            delta  = userObj.expiry_date - timezone.now()
            if  delta.total_seconds() <=0 and not request.user.is_superuser:
                messages.error(request, "Your account has expired.")
                # if request.user.is_authenicated
                logout(request)

            print("user not expired")
            # else :
                # print("user expired")
        response = self.get_response(request)
        return response