import os
from domain.images import Image
from shared.infrastructure.s3_repository import S3Repository

class DownloadImageUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def remove_downloaded_object(self, path):
        if os.path.exists(path):
            os.remove(path)
        

    def execute(self, resourceKey, path, bucket_name):
        image = Image(resourceKey=resourceKey, path=path)
        self.file_repository.download_object(local_path=path, bucket_name=bucket_name, resourceKey=resourceKey)