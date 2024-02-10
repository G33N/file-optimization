import os
from dotenv import load_dotenv
from tqdm import tqdm
from application.images.upload import UploadImageUseCase
from application.images.download import DownloadImageUseCase
from application.images.remove import RemoveImageUseCase
from application.images.list_all_objects import ListAllObjectsUseCase
from infrastructure.compress_images import compress_image, remove_output_files
from infrastructure.repositories.s3_repository import S3Repository

load_dotenv()

def main():
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = "BucketName"

    compression_quality = os.getenv('COMPRESSION_QUALITY')

    output_image_path = "output/"
    repository = S3Repository(aws_access_key, aws_secret_key)

    upload_image_use_case = UploadImageUseCase(repository)
    download_image_use_case = DownloadImageUseCase(repository)
    remove_image_use_case = RemoveImageUseCase(repository)
    list_all_objects = ListAllObjectsUseCase(repository)

    keys_to_download = list_all_objects.execute(bucket_name=aws_bucket_name)

    filtered_keys = [key for key in keys_to_download if not key.lower().endswith(".webp")]

    for key in tqdm(filtered_keys, desc="Processing s3 files", unit="image"):
        
        local_path = f"download/{key}"
        bucket_name = aws_bucket_name

        try:
            download_image_use_case.execute(resourceKey=key, path=local_path, bucket_name=bucket_name)
            print(f"Downloaded image: {key}")
            local_path = f"download/{key}"
            resourceKeyToUpload = compress_image(input_path=local_path, output_path=output_image_path, quality=compression_quality, format="WEBP")
            isSuccessUploaded = upload_image_use_case.execute(resourceKey=resourceKeyToUpload, bucket_name=bucket_name, path=output_image_path + resourceKeyToUpload)
            if isSuccessUploaded:
                print(f"Uploaded image: {resourceKeyToUpload}")
                remove_image_use_case.execute(resourceKey=key, bucket_name=bucket_name)
                remove_output_files(output_path=output_image_path+resourceKeyToUpload)
                print(f"Removed image: {key}")
            
        except Exception as e:
            print(f"Error downloading image {key}: {e}")
    
        finally:
            download_image_use_case.remove_downloaded_object(path=local_path)
            print(f"Removed downloaded object for {key}")


if __name__ == "__main__":
    main()