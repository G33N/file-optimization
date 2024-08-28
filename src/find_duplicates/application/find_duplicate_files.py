from tqdm import tqdm
from shared.infrastructure.s3_repository import S3Repository
from shared.infrastructure.database_repository import DatabaseRepository
from find_duplicates.application.check_path_priority import CheckPathPriorityUseCase
from find_duplicates.application.get_object_url import GetObjectUrlUseCase


class FindDuplicateFilesUseCase:
    def __init__(self, file_repository, database_repository):
        self.file_repository: S3Repository = file_repository
        self.database_repository: DatabaseRepository = database_repository
        self.check_path_priority_use_case = CheckPathPriorityUseCase(database_repository)
        self.get_object_url_use_case = GetObjectUrlUseCase(file_repository)

    def execute(self, resources):
        etags = {}
        duplicates = []

        for resource in tqdm(resources, desc="Finding duplicated files", unit="files"):
            etag = resource.get('etag')
            key = resource.get('resourceKey')
            path = self.get_object_url_use_case.execute(bucket_name=self.file_repository.get_bucket_name(), resourceKey=key)
            last_modified = resource.get('lastModified')

            if etag in etags:
                duplicate_resource = {
                    'etag': etag,
                    'resourceKey': key,
                    'path': path
                }
                if etags[etag]['resourceKey'] not in [dup['resourceKey'] for dup in duplicates]:
                    if not self.check_path_priority_use_case.execute(duplicate_resource['path']):
                        duplicates.append(duplicate_resource)
            else:
                etags[etag] = {'resourceKey': key, 'lastModified': last_modified}
        return duplicates
    