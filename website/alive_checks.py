import logging

from django.core.files.storage import default_storage
from django_alive import HealthcheckFailure


log = logging.getLogger(__name__)

def check_default_storage(filename: str) -> None:
    if not default_storage.exists(filename):
        log.exception("File %s does not exist", filename)
        raise HealthcheckFailure("Default storage error")