from infrastructure.repositories.s3_repository import S3Repository

class ListAllObjectsUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, bucket_name):
        return self.file_repository.read_all_objects(bucket_name=bucket_name)

