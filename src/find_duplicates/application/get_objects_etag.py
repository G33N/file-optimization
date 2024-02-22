from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from tqdm import tqdm
from shared.infrastructure.s3_repository import S3Repository

class GetObjectsEtagUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self, bucket_name,resourcesKey):
        etag_info = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.file_repository.get_head_object, bucket_name, resourceKey) for resourceKey in tqdm(resourcesKey, desc="Processing files", unit="files")]

            wait(futures)

            for future, resourceKey in zip(futures, resourcesKey):
                try:
                    s3_resp = future.result()
                    etag = s3_resp['ETag'].strip('"')
                    etag_info.append({'etag': etag, 'resourceKey': resourceKey})
                except Exception as e:
                    print(f"Error processing image: {e}")

        return etag_info