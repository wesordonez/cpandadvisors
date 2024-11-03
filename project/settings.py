"""
Django settings for CP&Advisors Web-Site project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import json
import base64
# import environ
 
import dj_database_url
from email.headerregistry import Address

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key

from google.oauth2 import service_account

from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(os.path.join(BASE_DIR), '.env')
load_dotenv(dotenv_path)

# Cloud Platform Settings
cloud_platform = os.environ.setdefault('CLOUD_PLATFORM', '')

# FIREBASE_CRED_PATH = env('FIREBASE_CRED_PATH')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# SECURITY WARNING: Delete this line after setting up the environment variables
# print(f"SECRET KEY:", get_random_secret_key())

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')

else:
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')


# Cloud Platform Settings
# if not DEBUG and cloud_platform in ['DIGITAL_OCEAN', 'RAILWAY']:
#     # since the firebase-cred cannot be uploaded manually 
#     # https://www.digitalocean.com/community/questions/how-to-upload-a-secret-credential-file
#     firebase_cred = env('FIREBASE_ENCODED')
#     decoded_bytes = base64.b64decode(firebase_cred)
#     decoded_json = json.loads(decoded_bytes.decode('utf-8'))
  
#     with open(FIREBASE_CRED_PATH, 'w') as f:
#         json.dump(decoded_json, f, indent=4)


ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]

# if not DEBUG:
#     CORS_ALLOWED_ORIGINS = os.environ.get('ALLOWED_CORS').replace(' ', '').split(',')

#     CORS_ORIGIN_WHITELIST = os.environ.get('ALLOWED_CORS').replace(' ', '').split(',')
#     CSRF_TRUSTED_ORIGINS = os.environ.get('ALLOWED_CORS').replace(' ', '').split(',')


PROJECT_TITLE = 'CP & Advisors' # name of the project

if DEBUG:
    DOMAIN = "http://localhost:8000"

else:
    DOMAIN = os.environ.get('DOMAIN')


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',  # sitemaps 
    'django.contrib.sitemaps',  # sitemaps 


    # 3rd party
    'tailwind',
    'corsheaders',
    'django_browser_reload',

    'styling',

    #first party
    'user',
    'blog',
    'inquiry',
]


SITE_ID = 1 # for sitemaps
ANALYTICS_TAG_ID = os.environ.get('GOOGLE_ANALYTICS') # for analytics tag on frontend

AUTH_USER_MODEL = "user.User" 


LOGIN_REDIRECT_URL = '/'

TAILWIND_APP_NAME = 'styling'


INTERNAL_IPS = [
    "127.0.0.1",
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware', #whitenoise
    'django_browser_reload.middleware.BrowserReloadMiddleware', # reload
    'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'project.urls'

# Email Settings

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # This is only for development
    # EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

else: 
    pass
    # uncomment below for production emailing
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # for production

    # EMAIL_HOST = env('EMAIL_HOST') #eg: smtpout.secureserver.net
    # EMAIL_PORT = 465

    # EMAIL_HOST_USER = env('EMAIL_HOST_USER') # eg: info@mail.com
    # EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

    # DEFAULT_FROM_EMAIL = Address(display_name=env('EMAIL_HOST_USER'), addr_spec=EMAIL_HOST_USER)

    # EMAIL_USE_SSL = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath("templates"),
            BASE_DIR.joinpath("templates", "html"),
            BASE_DIR.joinpath("templates", "html", "error"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custom_tags': 'project.templatetags.custom_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('DJANGO_ENV') == 'production':
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('PRD_SQL_ENGINE'),
            'NAME': os.environ.get('PRD_SQL_NAME'),
            'USER': os.environ.get('PRD_SQL_USER'),
            'PASSWORD': os.environ.get('PRD_SQL_PASSWORD'),
            'HOST': os.environ.get('PRD_SQL_HOST'),
            'PORT': os.environ.get('PRD_SQL_PORT')
        }
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': os.environ.get('SQL_ENGINE'),
                'NAME': os.environ.get('SQL_NAME'),
                'USER': os.environ.get('SQL_USER'),
                'PASSWORD': os.environ.get('SQL_PASSWORD'),
                'HOST': os.environ.get('SQL_HOST'),
                'PORT': os.environ.get('SQL_PORT')
            }
        }

    # DATABASES  = {
    #                 'default':dj_database_url.config(default=os.environ.get('POSTGRES_URL')),   
    #             }
    # DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles', 'static')
STATICFILES_DIRS = [
                        BASE_DIR.joinpath('templates'),
                        # BASE_DIR.joinpath('templates', 'js'),
                        # BASE_DIR.joinpath('templates', 'css'),
                        BASE_DIR.joinpath('templates', 'assets'),
                    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR.joinpath('media')


# GC_PROJECT_ID = env("PROJECT_ID") # google cloud project id

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_DOMAIN = 'http://localhost:8000'
   
else:
    MEDIA_URL = '/media/'

# Define the storage settings for media files
# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# GS_BUCKET_NAME = env("BUCKET_NAME") # google storage - GS
# GS_PROJECT_ID = env("PROJECT_ID")
# GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#     BASE_DIR.joinpath(env("FIREBASE_CRED_PATH"))
# )
# GS_DEFAULT_ACL = "publicRead"  # Optional: Set ACL for public access
# GS_QUERYSTRING_AUTH = True  # Optional: Enable querystring authentication
# GS_FILE_OVERWRITE = False # prevent overwriting


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

        # Send info messages to syslog
        # 'syslog':{
        #     'level':'INFO',
        #     'class': 'logging.handlers.SysLogHandler',
        #     'facility': SysLogHandler.LOG_LOCAL2,
        #     'address': '/dev/log',
        #     'formatter': 'verbose',
        # },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'mail_admins', 'celery'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}