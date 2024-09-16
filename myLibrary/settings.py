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
# print(IPAddr)
ALLOWED_HOSTS = ["*",IPAddr]


# Application definition

INSTALLED_APPS = [

    'jazzmin',
    # 'grappelli',
        # "admin_interface"
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
    'rest_framework',
     'rest_framework.authtoken',
    # -------
    'customAdmin',
    'booking',
    'students'
]

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
TEMPLATES = os.path.join(BASE_DIR,"templates")
# print(TEMPLATES)
ROOT_URLCONF = 'myLibrary.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ TEMPLATES,],
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # 'customAdmin.context_processors.jazzmin_usermenu_links',
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
# print(os.getenv('DEVLOPMENT'))
if os.getenv('DEVLOPMENT')=="TRUE":
    dbuser = 'root'
    PASSWORD ='Ra&5_153'
else :
    dbuser = 'samar'
    PASSWORD ='Samar@65535101'

DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.mysql',  
            'NAME': 'library_manger',  
            'USER': dbuser,  
            'PASSWORD': PASSWORD,  
            'HOST': 'localhost',  
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

USE_TZ = False
 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'   
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media") 


STATIC_DIR= os.path.join(BASE_DIR,'static')



STATICFILES_DIRS=[ STATIC_DIR,   ] 

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'customAdmin.CustomUser'

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]


from .jazzmin_settings import ui_settings,ui_tweaks_setting
JAZZMIN_SETTINGS = ui_settings


JAZZMIN_UI_TWEAKS = ui_tweaks_setting