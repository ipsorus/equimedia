"""
Django settings for equi_media_portal project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rsqzrx)%d)f^50@!kf=5e2j3(xswm#ntxt=%dh9e$nrbniw_d*'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
#
# ALLOWED_HOSTS = ['ipsoru68.beget.tech', 'www.ipsoru68.beget.tech']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'advertisements.apps.AdvertisementsConfig',
    'account.apps.AccountConfig',
    'event.apps.EventConfig',
    'portal.apps.PortalConfig',
    'articles.apps.ArticlesConfig',
    'news.apps.NewsConfig',
    'slider.apps.SliderConfig',
    'testimonial.apps.TestimonialConfig',
    'blog.apps.BlogConfig',
    'django_ckeditor_5',
    'el_pagination',
    'mptt',
    'services',
    'corsheaders',
    'bootstrap_modal_forms',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'equi_media_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'portal.context_processors.website_settings',
                'portal.context_processors.load_settings',
                'portal.context_processors.advertisement_settings',
                'portal.context_processors.contacts_settings',
                'portal.context_processors.about_us_settings',
                'portal.context_processors.socials_settings',
                'portal.context_processors.news_settings',
                'portal.context_processors.articles_settings',
                'portal.context_processors.slider_settings',
                'portal.context_processors.blog_settings',
                'django.template.context_processors.request', ## For EL-pagination
            ],
        },
    },
]

WSGI_APPLICATION = 'equi_media_portal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ipsoru68_equip',
# 	      'USER': 'ipsoru68_equip',
#         'PASSWORD': 'Zxcv0987',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'equimedia',
        'USER': 'admin',
        'PASSWORD': 'zxcv0987',
        'HOST': 'localhost',
        'PORT': '5432',
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'users.authentication.EmailAuthBackend',
]

LOGIN_URL = 'main'
LOGOUT_URL = 'main'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]


PER_PAGE = 9

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = 'ipsorus@yandex.ru'
EMAIL_HOST_PASSWORD = 'ovbgwvlbwfnrugho'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'pdf', 'png', 'jpg', 'gif', 'bmp', 'webp', 'tiff']
CKEDITOR_5_FILE_STORAGE = 'services.utils.CkeditorCustomStorage'
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "ru",
        "upload_file_types": ['jpeg', 'pdf', 'png', 'jpg', 'gif', 'bmp', 'webp', 'tiff'],
        'toolbar': {
            'items': [
                '|', 'heading',
                '|', 'outdent', 'indent',
                '|', 'bold', 'italic', 'link', 'underline', 'strikethrough', 'code', 'subscript', 'superscript',
                'highlight',
                '|', 'codeBlock', 'insertImage', 'bulletedList', 'numberedList', 'todoList',
                '|', 'blockQuote',
                '|', 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',
                '|',
            ],
            'shouldNotGroupWhenFull': True
        },
        "image": {
            "toolbar": [
                '|', "imageTextAlternative",
                "|", "imageStyle:alignLeft", "imageStyle:alignRight", "imageStyle:alignCenter", "imageStyle:side",
                "|", "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
    },
}