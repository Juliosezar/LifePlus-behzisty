from pathlib import Path
import environ
from os import path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool,False),
    ALLOWED_HOSTS=(list, []),
    DB_PORT=(int, 5432),
    IN_PRODUCTION=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env("SECRET_KEY") 
DEBUG = env("DEBUG")
IN_PRODUCTION = env("IN_PRODUCTION")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

if IN_PRODUCTION:
    # === SECURITY ===
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True          # Force HTTPS (optional)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [*ALLOWED_HOSTS]

    # Optional: HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True



AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
AWS_SERVICE_NAME = "s3"

if IN_PRODUCTION:
    STORAGES = {
        # Default storage for user-uploaded media files
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                # All options for this backend are passed here
                "location": "media", # Puts files in a 'media/' folder
                "file_overwrite": False, # Prevents overwriting files with the same name
                "default_acl": "private", # Makes media files publicly accessible
                "querystring_auth": False,
                "custom_domain": False,
                "querystring_expire": 3600,
            },
        },
        # Storage for static files, used by `collectstatic`
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "static", # Puts files in a 'static/' folder
                "default_acl": "public-read", # Makes static files publicly accessible
            },
        },
    }
else:
    STORAGES = {
        # Default storage for user-uploaded media files
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                # All options for this backend are passed here
                "location": "media", # Puts files in a 'media/' folder
                "file_overwrite": False, # Prevents overwriting files with the same name
                "default_acl": "private", # Makes media files publicly accessible
                "querystring_auth": False,
                "custom_domain": False,
                "querystring_expire": 3600,
            },
        },

        # Storage for static files, used by `collectstatic`
        "staticfiles": {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    }
    }




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_jalali", # jalali date support
    'accounts.apps.AccountsConfig',
    'cases.apps.CasesConfig',
    'reports.apps.ReportsConfig',
]

JALALI_SETTINGS = {
    # JavaScript static files for the admin Jalali date widget
    "ADMIN_JS_STATIC_FILES": [
        "admin/jquery.ui.datepicker.jalali/scripts/jquery-1.10.2.min.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js",
        "admin/jquery.ui.datepicker.jalali/scripts/calendar.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js",
        "admin/main.js",
    ],
    # CSS static files for the admin Jalali date widget
    "ADMIN_CSS_STATIC_FILES": {
        "all": [
            "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            "admin/css/main.css",
        ]
    },
}

DATE_INPUT_FORMATS = [
    '%Y-%m-%d',          # '1400-01-01'
    '%Y/%m/%d',          # '1400/01/01' (This is what your picker sends)
    '%Y-%m-%d %H:%M:%S',
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

ROOT_URLCONF = 'LifePlus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LifePlus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USERNAME'),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env('DB_HOST'),   # or your DB host
        'PORT': env('DB_PORT'),       
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/accounts/login/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


if IN_PRODUCTION:
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_DIRS = [BASE_DIR / 'static',]
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'

AUTH_USER_MODEL = 'accounts.User'

MEDIA_URL = '/media/'



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
