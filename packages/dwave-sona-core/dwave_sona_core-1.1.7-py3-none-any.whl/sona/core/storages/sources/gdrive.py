from urllib.parse import parse_qs, urlparse

from sona.settings import settings

from .base import SourceBase

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    pass


class GoogleDriveSource(SourceBase):
    info = settings.SONA_SOURCE_GOOGLE_SERVICE_ACCOUNT_INFO

    @classmethod
    def download(cls, file):
        credentials = service_account.Credentials.from_service_account_info(cls.info)
        service = build("drive", "v3", credentials=credentials)
        file_id = parse_qs(urlparse(file.path).query).get("id", [""])[0]
        metadata = service.files().get(fileId=file_id).execute()
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

        tmp_path = cls.tmp_dir / metadata["name"]
        with open(tmp_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                _status, done = downloader.next_chunk()
        return file.mutate(path=str(tmp_path))

    @classmethod
    def verify(cls, file):
        return file.path and file.path.startswith("https://drive.google.com")
