"""
Django settings for ITI3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a3pn^_=*+xi%*nv1zi+zx^!t$xbznpq%-d4*m6u=mwe6!sjzg_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Template settings

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['<username>.pythonanywhere.com']



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',

    # my app
    'TheArtVillage',

    #third party apps
    'reportlab',
    'django_countries'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',

)



ROOT_URLCONF = 'ITI3.urls'

WSGI_APPLICATION = 'ITI3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


LOGIN_URL = '/index/login/'

# MEDIA SETTINGS
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC SETTINGS
STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'  # You may find this is already defined as such.

STATICFILES_DIRS = (
    STATIC_PATH,
)

# Session cookies will last for half an hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CART_SESSION_ID='cart'

# CART Context processor
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
                'cart.context_processors.cart',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)