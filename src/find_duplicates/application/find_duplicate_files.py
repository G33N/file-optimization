from tqdm import tqdm
from shared.infrastructure.s3_repository import S3Repository

class FindDuplicateFilesUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, resources):
        etags = {}
        duplicates = []

        for resource in tqdm(resources, desc="Processing files", unit="files"):
            etag = resource.get('etag')
            key = resource.get('resourceKey')

            if etag in etags:
                duplicate_resource = {
                    'etag': etag,
                    'resourceKey': key
                }
                duplicates.append(duplicate_resource)
            else:
                etags[etag] = key

        return duplicates