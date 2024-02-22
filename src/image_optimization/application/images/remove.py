from shared.infrastructure.s3_repository import S3Repository

class RemoveImageUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, resourceKey, bucket_name):
        self.file_repository.remove_object(bucket_name=bucket_name, resourceKey=resourceKey)