import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ALLOWED_HOSTS = ['*']

ASGI_APPLICATION = "recipes_django.routing.application"

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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv("DB_NAME", "recipes_database.sqlite3"),
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') in ('True', 'true', '1', 'TRUE')

if DEBUG:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.getenv("REDIS_HOST", "Invalid redis host"), os.getenv("REDIS_PORT", "Invalid redis port"))],
            },
        },
    }

DEBUG_TOOLBAR = os.getenv('DEBUG_TOOLBAR') in (
    'True', 'true', '1', 'TRUE')

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

FIXTURE_DIRS = (
    'recipes_app/fixtures/',
)

# Application definition
INSTALLED_APPS = [
    'recipes_app.apps.RecipesAppConfig',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
if DEBUG:
    INSTALLED_APPS.append('django_extensions')

INTERNAL_IPS = [
    '127.0.0.1',
]

LANGUAGE_CODE = 'en-us'

MEDIA_ROOT = os.getenv('MEDIA_ROOT')
if MEDIA_ROOT:
    MEDIA_ROOT=MEDIA_ROOT.replace("$(pwd)", os.path.realpath(os.path.dirname(BASE_DIR)))

MEDIA_URL = os.getenv('MEDIA_URL')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG_TOOLBAR:
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ]
}

ROOT_URLCONF = 'recipes_django.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (os.getenv('SECRET_KEY')
              if os.getenv('SECRET_KEY')
              else 'LrPbLdXNCxagIgtUzoIWPeQAJxFQAwGoxqRZSCodxOgOtofHvEcJnXUOvKYoaWjNPdfzFwtomHLnFyFUrtSKeHIMgkMpYjgaTHhI')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = './django_static/'

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Templates')],
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

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
