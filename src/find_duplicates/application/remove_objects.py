from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from shared.infrastructure.s3_repository import S3Repository

class RemoveObjectsUseCase:
    def __init__(self, file_repository):
        self.file_repository: S3Repository = file_repository

    def execute(self,bucket_name, resourcesKey):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.file_repository.remove_object, bucket_name, resource['resourceKey']) for resource in tqdm(resourcesKey, desc="Deleting files", unit="files")]

            wait(futures)

            for future in futures:
                try:
                    return
                except Exception as e:
                    print(f"Error processing image: {e}")