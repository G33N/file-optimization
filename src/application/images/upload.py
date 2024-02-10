from domain.images import Image
from infrastructure.repositories.s3_repository import S3Repository

class UploadImageUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, resourceKey, path, bucket_name):
        image = Image(resourceKey, path, bucket_name)
        return self.file_repository.upload_object(local_path=path, bucket_name=bucket_name, resourceKey=resourceKey)