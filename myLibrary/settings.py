"""
Django settings for myLibrary project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# from jazzminsettings import jazzmin_setting

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = "876767hvvb^%&^$&BT&UJVJGYT%UUTGHF^%$hgfyt655rfgr65rf"
# DATABASE_URL = os.getenv('DATABASE_URL')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv('DEBUG') == 'True'
DEBUG = True


import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)
ALLOWED_HOSTS = ["*",IPAddr]


# Application definition

INSTALLED_APPS = [

    'jazzmin',
    # 'grappelli',
    "admin_interface",
    'django.contrib.admin',
    'corsheaders',
    "colorfield",
    'flat_responsive',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # 'django_group_model',

    # 'admin_reorder',
    'customAdmin',
    'booking',
]
ADMIN_REORDER = (
    # Keep original label and models
    # 'sites',

    {'app': 'booking', 'models': ({'model':'booking.Location','label':"Libraies"}, 'booking.Seat', 'booking.Student', 'booking.MonthlyPlan','booking.Payment','booking.theme')},
    # # Rename app
    # {'app': 'booking', 'label': 'Management'},


    # # Reorder app models

    # {'app': 'customAdmin', 'label': "Handle User"},

    # {'app': 'admin_interface', 'label': 'Theme selector',},

    # {'app': 'auth', 'label': 'Group'},
   
    # {'app': 'admin_intrface', 'models': ('auth.Groups','customAdmin.Users')},

    # {'app': 'admin_intrface', 'models': ('admin_intrface.theme','auth.Groups')},

    # # Exclude models

    # # Cross-linked models
    # {'app': 'auth', 'models': ('auth.User', 'sites.Site')},

    # # models with custom name
    # {'app': 'auth', 'models': (
    #     'auth.Group',
    #     {'model': 'auth.User', 'label': 'Staff'},
    # )},
)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]
# CORS_ALLOWED_ORIGINS = ["*"]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this line
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #  'admin_reorder.middleware.ModelAdminReorder',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'customAdmin.expirymiddleware.CheckUserExpiryMiddleware',
]
TEMPLATES = os.path.join(BASE_DIR,"templates")
print(TEMPLATES)
ROOT_URLCONF = 'myLibrary.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ TEMPLATES,],
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myLibrary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

os.getenv('DATABASE_URL')
# DATABASES = {  
#     'default': {  
#         'ENGINE': 'django.db.backends.mysql',  
#         'NAME': os.getenv('DATABASE_NAME'),  
#         'USER': os.getenv('DATABASE_USER'),  
#         'PASSWORD': os.getenv('DATABASE_PASSWORD'),  
#         'HOST': os.getenv('DATABASE_HOST'),  
#         'PORT': os.getenv('DATABASE_PORT'),
#         'OPTIONS': {  
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
#         }  
#     }  
# }  
print(os.getenv('DEVLOPMENT'))
if os.getenv('DEVLOPMENT')=="TRUE":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else :
    DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.mysql',  
            'NAME': 'library_manager',  
            'USER': 'samar',  
            'PASSWORD': 'Samar@65535101',  
            'HOST': '157.173.221.214',  
            'PORT': 3306,
            'OPTIONS': {  
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
            }  
        }  
    }  


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True
 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'   
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_DIR=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS=[  STATIC_DIR,   ] 

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CACHES = {
#     # ...
#     "admin_interface": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "TIMEOUT": 60 * 5,
#     },
#     # ...
# }

AUTH_USER_MODEL = 'customAdmin.CustomUser'
# JAZZMIN_SETTINGS = jazzmin_setting

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]