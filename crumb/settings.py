"""
Django settings for crumb project.
"""

import os
import dj_database_url

if os.path.isfile("env.py"):
    import env

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = 'DEVELOPMENT' in os.environ

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".herokuapp.com",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "home",
    "products",
    "cart",
    "checkout",

    "widget_tweaks",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    "cloudinary",
    "cloudinary_storage",
]

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'crumb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.contexts.cart_contents',
            ],
        },
    },
]

WSGI_APPLICATION = 'crumb.wsgi.application'


# DATABASE
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# ✅ TEK STORAGES (FIXED)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WH_SECRET = os.environ.get("STRIPE_WH_SECRET")

STRIPE_CURRENCY = "gbp"


ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_SIGNUP = True
ACCOUNT_LOGOUT_ON_GET = True


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = "Crumb <crumbcoffeelondon@gmail.com>"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

ACCOUNT_ADAPTER = "crumb.account_adapter.AccountAdapter"