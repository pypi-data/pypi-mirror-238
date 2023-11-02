import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .base import BaseService

SCOPES = ['https://www.googleapis.com/auth/drive']


class DriveService(BaseService):

    def __init__(
        self
    ) -> None:
        credentials, project = google.auth.default(scopes=SCOPES)
        self.drive_service = build('drive', 'v3', credentials=credentials)
        super().__init__(log_name="drive.service")

    def upload_google_doc(self, file_name: str, mime_type: str):
        """Insert new file.
        Returns : ID of the file uploaded
        """

        file_metadata = {'name': file_name, 'mimeType': 'application/vnd.google-apps.document'}
        media = MediaFileUpload(file_name, mimetype=mime_type)
        file = self.drive_service.files().create(
            body=file_metadata, media_body=media,
            fields='id'
        ).execute()

        return file.get('id')

    def export_pdf(self, file_id: str):
        """Download a Document file in PDF format.
        Args:
            file_id : file ID of any workspace document format file
        Returns : IO object with location
        """
        request = self.drive_service.files().export_media(
            fileId=file_id,
            mimeType='application/pdf'
        )
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        return file.getvalue()

    def delete_file(self, file_id):
        self.drive_service.files().delete(fileId=file_id).execute()
