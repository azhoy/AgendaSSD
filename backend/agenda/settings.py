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
import socket
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# PRODUCTION ENVIRONMENT VARIABLES
SECRET_KEY = 'qk3yb3H5dLDD@Y8v9Y$R8Zuk2tTTuVqykKxD@Fbd5PmZKdSaYQtQf9HCFd$xWuAFmtkWw'
DEBUG = False

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    f'{ip_address}'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'djoser',
    'core',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
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
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
            # 'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle'
        ],
    # Rate limiting the API
        'DEFAULT_THROTTLE_RATES': {
            'anon': '60/minute',  # 5 request per minutes for unhauthenticated user
            'user': '250/minute'
        }
}

# JWT options

# openssl genrsa -out jwt-key 4096
RSA_SIGNING_KEY = Path(BASE_DIR / 'jwt-key').read_text()

# openssl rsa -in jwt-key -pubout > jwt-key.pub
RSA_VERIFYING_KEY = Path(BASE_DIR / 'jwt-key.pub').read_text()

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=3),
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
EMAIL_HOST_USER = "agenda.ssd.esi@gmail.com"
EMAIL_HOST_PASSWORD = "hcsbjxvqeqaeemmx"
ADMIN_EMAIL_ALERT = "beck.ragas0m@icloud.com"


# CAHCES for throtling (Rate limit)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}