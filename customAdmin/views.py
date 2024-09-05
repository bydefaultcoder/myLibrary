from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest,HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

from .profileform import ProfileForm
from django.utils import timezone
# import customAdmin

from .admin import admin_site,CustomUserAdmin
from .models import CustomUser
# Create your views here.

# def admin_login(request:HttpRequest):
#     try:
#         if request.user.is_authenticated:
#             return redirect('dashboard/')
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user_obj = User.objects.filter(username = username)

#             if  not user_obj.exists () :
#                 messages.info(request,'Account not found')
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
#             user_obj = authenticate(username=username,password = password)

#             if user_obj and user_obj.is_superuser:
#                 login(request,user_obj)
#                 return redirect('dashboard/')
#             messages.info(request,'Invalid Password')
#             return redirect('/')
#         return render(request,'customadmin/loginform.html')
            
#     except Exception as e:
#         print(e)
#         return HttpResponse('Server Error')
# @staff_member_required
# def profile(request:HttpRequest):
#     return render(request,'admin/profile.html')


# from .customMixin import UserProfilePermissionMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import DetailView
@login_required
def display_profile(request):
    user = request.user
    ex_d = user.expiry_date - timezone.now()
    seconds_remain = ex_d.total_seconds()
    if seconds_remain <3600:
        ex_d_mess = f" { int((seconds_remain/60))} Minutes remain. Hurry Up Please Pay Increase Validity 😨"
    elif seconds_remain < 24*3600:
        ex_d_mess = f" { int((seconds_remain/3600))} Hours remain. Hurry Up Please Pay Increase Validity 🥺"
    elif seconds_remain < 7*24*3600:
        ex_d_mess = f" { int((seconds_remain/(24*3600)))} Days remain. Let's Increse The Validity 🙂"
    else :
        ex_d_mess = f" { int((seconds_remain/(24*3600)))} Days remain. Have a Nice Day 🙂🤩."
        
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('/admin/user-profile/')  # Replace 'admin_profile' with the name of your profile URL
    else:
        form = ProfileForm(instance=user)

    context = {
         **admin_site.each_context(request),  # Include the admin site context 
        'user': user,
        'form': form,
        'ex_d_mess' :ex_d_mess
    }
    return render(request, 'admin/profile.html', context)

from django.contrib.admin.models import LogEntry
from django.shortcuts import render

def recent_actions(request):
    recent_logs = LogEntry.objects.all().order_by('-action_time')[:10]
    context = {
         **admin_site.each_context(request),  # Include the admin site context 
         'admin_log': recent_logs
    }
    return render(request, 'admin/recent_actions.html', context)