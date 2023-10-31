from sona.settings import settings

from .base import StorageBase
from .local import LocalStorage
from .s3 import S3Storage


def create_storage():
    if settings.SONA_STORAGE_S3_SETTING:
        return S3Storage()
    return LocalStorage()
