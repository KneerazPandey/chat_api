from .base import *

DEBUG = False

ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chat_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 5432,
    }
}