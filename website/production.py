import os

from .settings import *


ALLOWED_HOSTS = [os.getenv('WEBSITE_HOSTNAME')] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = [f"https://{hostname}" for hostname in ALLOWED_HOSTS]
DEBUG = False

# Postgres connection info
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DBNAME'),
        'HOST': os.getenv('DBHOST'),
        'USER': os.getenv('DBUSER'),
        'PASSWORD': os.getenv('DBPASS'),
    }
}
