"""
Django settings for swiper project.

Generated by 'django-admin startproject' using Django 1.11.21.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c2n3$!&7ak1wd)(a9t^=iqk&d!v++q53w@bl*x&0oj8e%u7m5s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 添加身份验证中间件
    'common.middleware.AuthMiddleware',
]

ROOT_URLCONF = 'swiper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'swiper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swiper',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '12344321',
        'PORT': 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 缓存地址
        "LOCATION": "redis://127.0.0.1:6379/12",
        "OPTIONS": {
            'MAX_ENTRIES': 2000,
            # 使用线程池管理连接
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'user': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 缓存地址
        "LOCATION": "redis://127.0.0.1:6379/12",
        "OPTIONS": {
            'MAX_ENTRIES': 2000,
            # 使用线程池管理连接
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
