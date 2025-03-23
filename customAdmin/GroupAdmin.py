from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin
from django.utils.translation import gettext_lazy as _

class CustomGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        """Only Super Admins can see the Groups module"""
        return request.user.is_superuser  # 🔒 Only Super Admin can access Groups

    def has_view_permission(self, request, obj=None):
        """Only Super Admins can view Groups"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only Super Admins can edit Groups"""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Only Super Admins can add new Groups"""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Only Super Admins can delete Groups"""
        return request.user.is_superuser

