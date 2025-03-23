from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest,HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

from .profileform import ProfileForm
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from .admin import admin_site,CustomUserAdmin
from .models import CustomUser


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
    recent_logs = LogEntry.objects.filter(
            user=request.user,  # request.user will be an instance of CustomUser
            action_time__gte=now() - timedelta(days=7)  # Adjust the time range as needed
        ).select_related('content_type')[:10]  # Limiting to the last 10 actions
    context = {
         **admin_site.each_context(request),  # Include the admin site context 
         'admin_log': recent_logs
    }
    return render(request, 'admin/recent_actions.html', context)