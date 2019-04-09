"""
Django settings for facebookPages project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

CELERY_BROKER_URL = 'amqp://127.0.0.1'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=0@@tm@ph-$6d-oae883lcn-1gx2hz)02&s&$*0k9xkyj#(lj^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'facebook.apps.FacebookConfig',
    'dashboard',
    'django_extensions',
    #'sslserver',
]

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'facebook.backends.FacebookBackend',
    'accounts.backends.ManualSignupBackend',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_EXEMPT_URLS = (
    r'^login$',
    r'^accounts/signup/$',
    r'^reset$',
    r'^change/password$',
    r'^activate$',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dashboard.middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'facebookPages.urls'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hodos.analytix@gmail.com'
EMAIL_HOST_PASSWORD = 'analytix123'
EMAIL_PORT = 587

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'facebookPages.wsgi.application'

import dj_database_url


DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': os.environ.get('DB_NAME', 'fbapp'),
        # 'USER': os.environ.get('DB_USER', 'postgres'),
        # 'PASSWORD': os.environ.get('DB_PASSWORD', '123456789'),
        # 'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        # 'PORT': os.environ.get('DB_PORT', '5432'),
        # 'TEST': {
        #     'NAME': 'test_default',
        #     'USER': 'postgres',
        #     'PASSWORD': 'postgres',
        #     'HOST': 'db',
        #     'PORT': 5432
        # },
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'searchapp',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# DATABASES['default'] = dj_database_url.parse('postgres://jbubgbhpfbqqom:36bb1ca6f434c39f9566b9b69592050ea4b62f6c26c319697a13869130e43fdd@ec2-184-73-153-64.compute-1.amazonaws.com:5432/d6cnh865ap5r2p', conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CONSUMER_KEY= 'mqjmf3Tp4D8NGNDd5AR9dHKrT'

CONSUMER_SECRET = 'd3uPKttcEBYLPeyyrLIFRi45KzPCKcgeEMYs8kAo00gFk5egDD'

FACEBOOK_CONFIG = {
    'app_id': '1204217713050064',
    'app_secret': 'ef7e6acb9ef467dd10d739d51c9e6ab3',
    'redirect_uri': 'http://localhost:8000/dashboard/facebook_auth_handler/'
}