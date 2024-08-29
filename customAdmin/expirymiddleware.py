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
        
        today_time = timezone.now().date()
        # print("middleware is called")
        userObj = CustomUser.objects.get(pk=request.user.pk)
        # print(userObj.expiry_date )
        if  userObj.expiry_date:
            db_time = userObj.expiry_date.date()
            # print(today_time,db_time)
            # print(request.user.is_superuser)
            print(userObj.expiry_date.date(),timezone.now().date())
            if userObj.expiry_date.date() >= timezone.now().date() or request.user.is_superuser:
            # if True:
                print("user not expired")
                # if userObj.avatar:
                #     print(f"{userObj.avatar.url}")
                    # from django.conf import settings
                    # settings.JAZZMIN_SETTINGS["user_avatar"] = userObj.avatar.url
            else :
                # print("user expired")
                messages.error(request, "Your account has expired.")
                logout(request)
        response = self.get_response(request)
        return response