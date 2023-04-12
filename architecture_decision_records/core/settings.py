"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ADR_ROOT = os.getenv("ADR_ROOT", os.path.expanduser("~/.architecture_decision_records"))

# Set the swappable User model to the App custom User model
AUTH_USER_MODEL = "users.User"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv("ADR_ALLOWED_HOSTS", "*").split(" ")

SECRET_KEY = os.getenv("ADR_SECRET_KEY", "django-insecure-0w5!cas22(uo_@sz7yi33zw0b@1jd*j9!fu8u=o8w0mr+1ax1iv")

# Application definition

INSTALLED_APPS = [
    # contributed
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    # ...
    "corsheaders",
    "crispy_forms",
    "crispy_bootstrap5",
    "markdownify",
    # local
    # ...
    "architecture_decision_records.core",
    "architecture_decision_records.users",
    "architecture_decision_records.decisions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "architecture_decision_records.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "architecture_decision_records.core.wsgi.application"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = "home"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": os.getenv("ADR_DB_NAME", "adr"),  # Database name
        "USER": os.getenv("ADR_DB_USER", ""),  # Database username
        "PASSWORD": os.getenv("ADR_DB_PASSWORD", ""),  # Database password
        "HOST": os.getenv("ADR_DB_HOST", "localhost"),  # Database server
        "PORT": os.getenv("ADR_DB_PORT", ""),  # Database port (leave blank for default)
        "CONN_MAX_AGE": int(os.getenv("ADR_DB_TIMEOUT", "300")),  # Database timeout
        "ENGINE": os.getenv(
            "ADR_DB_ENGINE", "django.db.backends.postgresql"
        ),  # Database driver "postgresql"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(ADR_ROOT, "static")
STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "project-static"),)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MARKDOWNIFY_STRIP = False
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": ["a", "abbr", "acronym", "b", "blockquote", "em", "i", "li", "ol", "p", "strong", "ul"],
        "STRIP": False,
    }
}
