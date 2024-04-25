import os
import sys
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.infrastructure.s3_repository import S3Repository
from tqdm import tqdm
from application.images.upload import UploadImageUseCase
from application.images.download import DownloadImageUseCase
from application.images.remove import RemoveImageUseCase
from application.images.list_all_objects import ListAllObjectsUseCase
from infrastructure.compress_images import compress_image, remove_output_files


def process_image(key, aws_bucket_name, compression_quality, output_image_path, upload_image_use_case, download_image_use_case, remove_image_use_case):
    local_path = f"download/{key}"

    try:
        download_image_use_case.execute(resourceKey=key, path=local_path, bucket_name=aws_bucket_name)
        print(f"Downloaded image: {key}")

        resource_key_to_upload = compress_image(key=key,input_path=local_path, output_path=output_image_path, quality=compression_quality, format="WEBP")
        isSuccessUploaded = upload_image_use_case.execute(resourceKey=resource_key_to_upload, bucket_name=aws_bucket_name, path=output_image_path + resource_key_to_upload)

        if isSuccessUploaded:
            print(f"Uploaded image: {resource_key_to_upload}")
            remove_image_use_case.execute(resourceKey=key, bucket_name=aws_bucket_name)
            remove_output_files(output_path=output_image_path + resource_key_to_upload)
            print(f"Removed image: {key}")

    except Exception as e:
        print(f"Error processing image {key}: {e}")

    finally:
        download_image_use_case.remove_downloaded_object(path=local_path)
        print(f"Removed downloaded object for {key}")

def display_welcome_message():
    print("CLI application developed by G33N for image optimisation !")
    print("---------------------------------------------------------")

def get_input(message):
    key = input(message+": ")
    return key


def main():
    display_welcome_message()

    aws_access_key = get_input("Enter your AWS_ACCESS_KEY_ID")
    aws_secret_key = get_input("Enter your AWS_SECRET_ACCESS_KEY")
    aws_bucket_name = get_input("Enter your AWS_BUCKET_NAME")
    compression_quality = get_input("Enter your COMPRESSION_QUALITY from 0 to 100")

    output_image_path = "output/"
    repository = S3Repository(aws_access_key, aws_secret_key)

    upload_image_use_case = UploadImageUseCase(repository)
    download_image_use_case = DownloadImageUseCase(repository)
    remove_image_use_case = RemoveImageUseCase(repository)
    list_all_objects = ListAllObjectsUseCase(repository)

    keys_to_download = list_all_objects.execute(bucket_name=aws_bucket_name)

    filtered_keys = [key for key in keys_to_download if not key.lower().endswith(".webp")]

    with ThreadPoolExecutor() as executor:
        futures = []

        for key in tqdm(filtered_keys, desc="Processing files", unit="image"):
            future = executor.submit(
                process_image,
                key,
                aws_bucket_name,
                compression_quality,
                output_image_path,
                upload_image_use_case,
                download_image_use_case,
                remove_image_use_case
            )
            futures.append(future)

        wait(futures)

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing image: {e}")

    executor.shutdown(wait=True)


if __name__ == "__main__":
    main()