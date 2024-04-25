from tqdm import tqdm
from shared.infrastructure.s3_repository import S3Repository

class FindDuplicateFilesUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, resources):
        etags = {}
        duplicates = []

        for resource in tqdm(resources, desc="Finding duplicated files", unit="files"):
            etag = resource.get('etag')
            key = resource.get('resourceKey')
            last_modified = resource.get('lastModified')

            if etag in etags:
                if last_modified > etags[etag]['lastModified']:
                    duplicate_resource = {
                        'etag': etag,
                        'resourceKey': etags[etag]['resourceKey']
                    }
                    duplicates.append(duplicate_resource)
                else:
                    etags[etag] = {'resourceKey': key, 'lastModified': last_modified}
            else:
                etags[etag] = {'resourceKey': key, 'lastModified': last_modified}

        return duplicates