"""
Django settings for servitelWeb project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailersend.net'
EMAIL_PORT = 587  # Puerto SMTP de MailerSend
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'MS_Pqwt9D@trial-o65qngkme93lwr12.mlsender.net'
EMAIL_HOST_PASSWORD = 'a48ae57f7109e7232c8ba2bfbfe1ffa9cd69416335cbcf6ebcfbbf456581b841'

MAILERSEND_API_KEY = 'mlsn.a48ae57f7109e7232c8ba2bfbfe1ffa9cd69416335cbcf6ebcfbbf456581b841'
DEFAULT_FROM_EMAIL = 'MS_Pqwt9D@trial-o65qngkme93lwr12.mlsender.net'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-vc4dhc_sc^cg^nw0s&*u(u%q(m34s0=1*kbxwn+igr*19=p5%^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("IS_DEVELOPMENT", True)

ALLOWED_HOSTS = [os.getenv('APP_HOST'), '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://www.servitelcctv.cl']

# os.getenv("APP_HOST"),
#                 '127.0.0.1'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crud',
    'login',

    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'servitelWeb.urls'

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

WSGI_APPLICATION = 'servitelWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  os.getenv('DATABASE_NAME'),
        'USER':  os.getenv('DATABASE_USER'),
        'PASSWORD':  os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT':  os.getenv('DATABASE_PORT'),
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
STATIC_ROOT = BASE_DIR / "staticfiles"

#Media Files
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'login.User'

AUTHENTICATION_BACKENDS = [
    'login.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',  # Backend predeterminado
]

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'