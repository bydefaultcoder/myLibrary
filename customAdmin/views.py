from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest,HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def admin_login(request:HttpRequest):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard/')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)

            if  not user_obj.exists () :
                messages.info(request,'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username,password = password)

            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return redirect('dashboard/')
            messages.info(request,'Invalid Password')
            return redirect('/')
        return render(request,'customadmin/loginform.html')
            
    except Exception as e:
        print(e)
        return HttpResponse('Server Error')
@staff_member_required
def profile(request:HttpRequest):
    return render(request,'admin/profile.html')
