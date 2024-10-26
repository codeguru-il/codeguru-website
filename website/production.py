import os

from .settings import *


ALLOWED_HOSTS = [os.getenv('WEBSITE_HOSTNAME')] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = [f"https://{hostname}" for hostname in ALLOWED_HOSTS]
DEBUG = False

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Postgres connection info
conn_str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get('AZURE_REDIS_CONNECTIONSTRING'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}
