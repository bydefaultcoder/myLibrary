from django.apps import AppConfig


class CustomadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customAdmin'
    # def ready(self):
    #     from django.contrib.auth.models import Permission
    #     from django.contrib.contenttypes.models import ContentType
    #     from .models import CustomUser

    #     Permission.objects.get_or_create(
    #         codename='view_own_profile',
    #         name='Can view own profile',
    #         content_type=ContentType.objects.get_for_model(CustomUser),
    #     )
