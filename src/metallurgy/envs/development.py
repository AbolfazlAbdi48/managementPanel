from .common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "metallurgy_db",
        'USER': "metallurgy_user",
        'PASSWORD': "123@456",
        'HOST': 'db',
        'PORT': 5432,
    }
}
