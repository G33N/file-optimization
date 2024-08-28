from shared.infrastructure.s3_repository import S3Repository

class GetObjectUrlUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, bucket_name, resourceKey):

        url = self.file_repository.get_object_url(bucket_name, resourceKey)

        return url

        