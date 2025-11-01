from azure.identity import DefaultAzureCredential

from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = (
    [os.getenv("WEBSITE_HOSTNAME"), *os.getenv("CUSTOM_HOSTNAMES", "").split(" ")]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)
CSRF_TRUSTED_ORIGINS = [f"https://{hostname}" for hostname in ALLOWED_HOSTS]
DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Add whitenoise middleware after the security middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# whitenoise static files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "token_credential": DefaultAzureCredential(),
            "account_name": os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
            "azure_container": "files",
        },
    },
    "submissions": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "token_credential": DefaultAzureCredential(),
            "account_name": os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
            "azure_container": "submissions",
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_ROOT,
        },
    },
}


# Postgres connection info
conn_str = os.getenv("CUSTOMCONNSTR_AZURE_POSTGRESQL_CONNECTIONSTRING")
conn_str_params = {pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(";")}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": conn_str_params["Database"],
        "HOST": conn_str_params["Server"],
        "USER": conn_str_params["User Id"],
        "PASSWORD": conn_str_params["Password"],
    }
}
