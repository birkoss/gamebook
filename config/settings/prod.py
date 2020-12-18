from .base import *


ALLOWED_HOSTS = ['']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DATABASE_NAME'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


STATIC_URL = 'https://cdn.birkoss.com/assets/api/'
STATIC_ROOT = '/home/birkoss/domains/cdn.birkoss.com/public_html/assets/api/'
