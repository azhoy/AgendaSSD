"""
Django settings for agenda project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# At least 512bits => Bc of HMAC SHA-512
# TODO: Set from Env Variables in prod (=> installation script)
SECRET_KEY = ')+e@9!)1e98&-=074+6&3b5d)7+))b(10f111-0-2bc13ded0@fb3b=1)d5**7=013=!*7f0*)cb00)ec@@d&8e*&!!b!)7cbb2e=a' \
             '38@b)fcfb&eac@71e9ca@2e@0)+++&+1c08**(=!f&0368@+b656+fc!563(b*e05*(a+7=df6&c(9+9af!476!!&3b9b9)-=(a-+8' \
             '8e(+-@!34&51d*-=0)=-ccb4@a6+41806ec!@83)a2fdf@=@4(08+3ea6*(8*d8+95fd&13!d52e528(9*2f!*)*64!e*a-75c9605' \
             '=))eebef1+dd3d21da@b@bd@3fa&+80+9(67c@bd0-1d=cc479@-4e&(+)35d-fc1=-f-2*(@96cb0+93b0+43+4-32f@9)9-)@=&+' \
             '35c50=((b!*(69c&2cb8c&d65c33f)ba!eba323a)9da@0a4)e2de!1&05a0510-d@1@7-*a+70&0a-9*&4d=9@30-6(@b5-e404f-@('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # TODO: Remove debug in production

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []  # TODO: Set in production

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'djoser',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
        'OPTIONS': {
            'min_length': 12,
        }
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

TIME_ZONE = 'Europe/Brussels'

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
    # JWT as default authentication system
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Render information as JSON
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

# JWT options

# TODO: Set in env variable genreated automattically
# openssl genrsa -out jwt-key 4096
RSA_SIGNING_KEY = Path(BASE_DIR / 'jwt-key').read_text()

# TODO: Set in env variable genreated automattically
# openssl rsa -in jwt-key -pubout > jwt-key.pub
RSA_VERIFYING_KEY = Path(BASE_DIR / 'jwt-key.pub').read_text()

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),  # TODO: CHANGE IN PROD !!!
    'REFRESH_TOKEN_LIFETIME': timedelta(days=6),  # TODO: CHANGE IN PROD !!!
    # A new refresh token is submitted when using the refresh token endpoint
    'ROTATE_REFRESH_TOKENS': True,
    # Causes refresh tokens submitted to the refresh endpoints to be added to the blacklist
    # Prevent them from being reused
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': RSA_SIGNING_KEY,
    'VERIFYING_KEY': RSA_VERIFYING_KEY,
    # The authorization header name to be used for authentication.
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # To send an authentication token to the server => Prefix the Token with JWT
    # FORMAT => Authorization: JWT <token>
    'AUTH_HEADER_TYPES': ('JWT',),
    # DB field included in the token, username is unique and cannot be changed
    'USER_ID_FIELD': 'username',
    # Name of the key to the USER_ID_FIELD in the token
    'USER_ID_CLAIM': 'username'
}
# Replacing the default auth model with the modified abstract model from models.py
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'core.User'

# Djoser serializers options
DJOSER = {
    'USER_ID_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    # URL to the frontend password reset page.
    # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    # URL to the frontend username reset page.
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    # URL to the frontend activation page.
    'ACTIVATION_URL': 'accounts/activate/{uid}/{token}',
    # Send activation link after creating an account or updating an email ?
    'SEND_ACTIVATION_EMAIL': True,
    # Send confirmation after register or activation ?
    'SEND_CONFIRMATION_EMAIL': False,
    # Send confirmation after password change
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # Send confirmation after username change
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'user': 'core.serializers.OtherUserSerializer',
        'current_user': 'core.serializers.UserSerializer',
    },
    'HIDE_USERS': False
}

# Argon2 used by default for storing password
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    # 'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'agenda.ssd.esi@gmail.com'  # TODO: Set in env variables
EMAIL_HOST_PASSWORD = 'hcsbjxvqeqaeemmx'  # TODO: Set in env variables
ADMIN_EMAIL_ALERT = 'beck.ragas0m@icloud.com'  # TODO: Set in env variables
