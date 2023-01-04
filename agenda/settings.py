"""
Django settings for agenda project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x443m1!zfpcc(!rk@&fis+h9yjv=mj9*pq--0vxd&)jpkl@y9*'  # TODO: Set from Evn Variables in prod (=> installation script)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # TODO: Remove debug in production

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []  #

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # 3rd
    'djoser',  # 3rd
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'agenda.urls'
TEMPLATE_CORE_DIR = BASE_DIR / 'core' / 'templates' / 'core'

# TEMPLATE_DIRS = [TEMPLATE_CORE_DIR]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_CORE_DIR],
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

WSGI_APPLICATION = 'agenda.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agenda',
        'USER': 'dbuser',
        'PASSWORD': 'P@$$w0rd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST framework options
REST_FRAMEWORK = {
    # Auto type conversion from str to decimal
    'COERCE_DECIMAL_TO_STRING': False,
    # Activate JSON Web token as default => TODO: Replace with Ayoub implementation
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # Closes all the API endpoints to anonymous users excepts registration and login
        #  'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # TODO: Remove in production
    ]
}


# JSON WEB TOKEN parameters =>  TODO: Replace with Ayoub implementation
SIMPLE_JWT = {
    # To send an authentication token to the server => Prefix the Token with JWT
    # JWT <token>
    'AUTH_HEADER_TYPES': ('JWT',),
    # Lifetime of the JSON Web Token
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),  # TODO: CHANGE IN PROD !!!
    'REFRESH_TOKEN_LIFETIME': timedelta(days=6),  # TODO: CHANGE IN PROD !!!

    'ROTATE_REFRESH_TOKENS': True,
    # Make sure the old refresh token can no longer be used
    'BLACKLIST_AFTER_ROTATION': True
}
# Replacing the default auth model with the modified abstract model from models.py
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'core.User'

# Djoser serializers options
DJOSER = {
    'SERIALIZERS': {
        # Custom User Serializers with 'id', 'username', 'password' and 'protected_symmetric_key' fields
        'user_create': 'core.serializers.UserCreateSerializer',
        'user': 'core.serializers.UserSerializer',
        'current_user': 'core.serializers.UserSerializer',
    }
}
