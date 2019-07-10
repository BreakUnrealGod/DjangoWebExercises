"""
Django settings for djangoday10 project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&s5ikoim&fxk@61(t5yj&&zz3ic4f9&rj)=s2tt*&nf)ms0d-p'

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
    'user.apps.UserConfig',
]

MIDDLEWARE = [
    # 站点缓存 ， 注意必须在第一个位置
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 站点缓存, 注意必须在最后一个位置
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'djangoday10.urls'

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

WSGI_APPLICATION = 'djangoday10.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django02day10',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 缓存到表中
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }


# 把数据给缓存到文件中
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'c:/foo/bar',
#     }
# }


# 使用本地的缓存系统
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 配置异步任务
BROKER_URL = 'redis://127.0.0.1:6379/6'

# 存储结果并跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'

# 消息格式
CELERY_ACCEPT_CONNECT=['application/json',]

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

# celery的时区
CELERY_TIMEZONE = TIME_ZONE


# 发送邮件的设置
EMAIL_HOST = 'smtp.126.com'
EMAIL_HOST_USER = 'student1902@126.com'
EMAIL_HOST_PASSWORD = 'student1902'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # 126,QQ: 465   163:454

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


LOG_PATH=os.path.join(BASE_DIR,'log')
if not os.path.join(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    # version只能为1,定义了配置文件的版本，当前版本号为1.0
    "version": 1,
    # True表示禁用logger
    "disable_existing_loggers": False,
    # 格式化
    'formatters': {
        'default': {
            'format': '%(levelno)s %(funcName)s %(module)s %(asctime)s %(message)s '
        },
        'simple': {
            'format': '%(levelno)s %(module)s %(created)s %(message)s'
        }
    },

    'handlers': {
        'user_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 指定文件大小
            'maxBytes': 5 * 1024,
            # 指定文件地址
            'filename': '%s/log.txt' % LOG_PATH,
            'formatter': 'default'
        },
        # 'uauth_handlers': {
        #     'level': 'DEBUG',
        #     # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     # 指定文件大小
        #     'maxBytes': 5 * 1024 * 1024,
        #     # 指定文件地址
        #     'filename': '%s/uauth.txt' % LOG_PATH,
        #     'formatter': 'simple'
        # }
    },
    'loggers': {
        'user': {
            'handlers': ['user_handlers'],
            'level': 'INFO'
        },
        # 'auth': {
        #     'handlers': ['uauth_handlers'],
        #     'level': 'INFO'
        # }
    },

    'filters': {

        }
}




