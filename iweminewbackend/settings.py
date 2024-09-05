"""
Django settings for iweminewbackend project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z1yhsit_&a3km53v0@7@4nvp*xsu@@u%vjg5&01)$%mgmpxi!@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'useraccount.User'

SITE_ID = 1

WEBSITE_URL = 'https://api.iwemiresearch.org'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKEN": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "acomplexkey"
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED= True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_EMAIL_NOTIFICATIONS =True

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_URL = "https//:127.0.0.1:8000/api/auth/login/"

JWT_AUTH_COOKIE = 'iwemiresearch-auth'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
    #    'rest_framework.permissions.IsAuthenticated',
    )

}

# if DEBUG:
#     REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
#         "rest_framework.authentication.SessionAuthentication"
#     )

CORS_ALLOWED_ORIGINS = [
    'https://127.0.0.1:8000',
    'https://127.0.0.1:3000',
    'http://localhost:5173',
    'http://localhost:5174',
    'https://iwemiresearch.org',
    'https://iwemiresearchnewfrontend.onrender.com',
    'https://*',
]

CORS_ALLOW_ALL_ORIGINS = True

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "REGISTER_SERIALIZER": "useraccount.serializers.CustomRegisterSerializer"
}                       

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'useraccount.serializers.CustomPasswordResetSerializer',
}

DJANGO_REST_AUTH = {
    'EMAIL_VERIFICATION': 'mandatory',  # or 'optional'
    'SERIALIZERS': {
        'REGISTER_SERIALIZER': 'useraccount.serializers.CustomRegisterSerializer',
    },
}

DJANGO_REST_AUTH_PASSWORD_RESET_CONFIRM = 'http://iweminewbackend.onrender.com/password/reset/confirm/{uid}/{token}'



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)



# Email server settings /////////////////////////////////////////////////////////////////////////////////////////////

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'box2458.bluehost.com'
EMAIL_HOST_USER = 'support@iwemiresearch.org'
EMAIL_HOST_PASSWORD = 'publisher123'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'support@iwemiresearch.org'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'corsheaders',

    'papers',
    'useraccount',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iweminewbackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'iweminewbackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = 'static/'

MEDIA_URL =  '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Stripe Settings //////////////////////////////////////////

STRIPE_PUBLIC_KEY = 'pk_test_51Pl654BtS3lVeLJEYpzqhlEkp4B9qmaX8ch4gJDslvwEm0kTw06sOZJ9Pc9J0VlC2wP2hiFqa0R43nHcXCwLFQWW00QtE9aDAU'
STRIPE_SECRET_KEY = 'sk_test_51Pl654BtS3lVeLJEyM36zEK5fBflWOA45UKmJHcxxkEg7lof2yyQSOOXrSGyGKj9ylPcGAsjfHThiS9eddfht7Mr001JYwVL0g'
