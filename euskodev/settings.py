from pathlib import Path
import os #Internacionalización
from django.utils.translation import gettext_lazy as _
import json
import getpass
from django.urls import reverse, reverse_lazy
import tempfile

from django.conf import global_settings #Internacionalización

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-672-=9w%pc2fch+g890ny#)vgnm9)-z)jo(e&*c+6!7sj@kzjs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applications.home',
    'applications.erp',# Asegúrate de que está aquí
    'rosetta',
    'tinymce',
    'django_recaptcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'euskodev.urls'


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

WSGI_APPLICATION = 'euskodev.wsgi.application'


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


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
BASE_URL = 'localhost'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR / "static"),
]




STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

"""STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)"""


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LANGUAGE_CODE = 'es'
# LANGUAGE_CODE = 'en-US'

LANGUAGES = (
    ('es', _('Español')),
    ('eu', _('Euskara')),
    #('en', _('English')),
    #('ca', _('Catalan')),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'es', },  # Spanish
        #{'code': 'en', },  # English
        #{'code': 'ca', },  # Catalan
        {'code': 'eu', },  # Basque
    ),
    'default': {
        'fallbacks': ['es'],
        'hide_untranslated': False,
    }
}


TINYMCE_DEFAULT_CONFIG = { 
    'height': 360,
    'width': 600,
    'plugins': 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount',
      'toolbar': 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help | fontsizeselect',
        'fontsize_formats': '8pt 10pt 12pt 14pt 15pt 16pt 17pt 18pt 24pt 36pt', }


"""===========================================
    esto es para la configuracion de correo 
=============================================="""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "Info@euskodev.eus"
EMAIL_HOST_PASSWORD = 'nqkg bxps wtjf xwcc '  # Usa la contraseña generada
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_CHARSET = 'utf-8'
EMAIL_USE_LOCALTIME = True  # Asegura que Django maneje bien la codificación


# Configuración de reCAPTCHA
RECAPTCHA_PUBLIC_KEY = "6LfjFPEqAAAAAL23CYZsif_KdPGU2189i0UMjIgk"
RECAPTCHA_PRIVATE_KEY = "6LfjFPEqAAAAABBc48ipUn3encwA_Ix350EJgQE1"

# Opcional: Para desactivar en desarrollo
RECAPTCHA_VERIFY_REQUESTS = False  # False si no quieres validar en local
