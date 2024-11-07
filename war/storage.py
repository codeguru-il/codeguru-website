import os

from django.core.files.storage import Storage, storages


def submissions_storage() -> Storage:
    return storages["submissions"]


def get_survivor_path(war_id: int | str, survivor_name: str) -> str:
    return os.path.join("wars", "submissions", str(war_id), "joined_submissions", survivor_name)
