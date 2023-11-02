from google.cloud import storage

from .base import BaseService


class StorageService(BaseService):
    def __init__(
        self,
        storage_client: storage.Client,
        bucket: str
    ) -> None:
        self.storage_client = storage_client
        self.bucket = storage_client.bucket(bucket)
        super().__init__(log_name='storage.service')

    def upload_file_from_memory(self, destination_file_name: str, contents) -> None:
        blob = self.bucket.blob(destination_file_name)
        blob.upload_from_string(contents)

