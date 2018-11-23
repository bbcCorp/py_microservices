from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './../../setup/test-data/db.sqlite3',
    }
}

EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'