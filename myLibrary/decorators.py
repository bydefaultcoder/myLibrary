from django.contrib.auth.decorators import login_required, user_passes_test

def role_required(*role_names):  # Accept multiple roles
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda user: user.groups.filter(name__in=role_names).exists())
        def wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator