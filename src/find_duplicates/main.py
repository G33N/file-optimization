import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.infrastructure.s3_repository import S3Repository
from find_duplicates.application.list_all_objects import ListAllObjectsUseCase
from find_duplicates.application.get_objects_etag import GetObjectsEtagUseCase
from find_duplicates.application.find_duplicate_files import FindDuplicateFilesUseCase
from find_duplicates.application.remove_objects import RemoveObjectsUseCase


def display_welcome_message():
    print("CLI application developed by G33N for find and remove duplicates!")
    print("-----------------------------------------------------------------")

def display_options():
    print("-----------------------------------------------------------------")
    print("Do you want to find and remove duplicates from your S3 bucket?")
    print("-----------------------------------------------------------------")

def get_input(message):
    key = input(message+": ")
    return key


def main():
    display_welcome_message()

    aws_access_key = get_input("Enter your AWS_ACCESS_KEY_ID")
    aws_secret_key = get_input("Enter your AWS_SECRET_ACCESS_KEY")
    aws_bucket_name = get_input("Enter your AWS_BUCKET_NAME")

    repository = S3Repository(aws_access_key, aws_secret_key)

    list_all_objects = ListAllObjectsUseCase(repository)
    get_objects_etag_use_case = GetObjectsEtagUseCase(repository)
    find_duplicate_files_use_case = FindDuplicateFilesUseCase(repository)
    remove_objects_use_case = RemoveObjectsUseCase(repository)


    keys_to_analice = list_all_objects.execute(bucket_name=aws_bucket_name)

    etags = get_objects_etag_use_case.execute(bucket_name=aws_bucket_name, resourcesKey=keys_to_analice)

    duplicateFiles = find_duplicate_files_use_case.execute(resources=etags)
    
    print(f"Duplicate files found: {duplicateFiles}")

    if len(duplicateFiles) == 0:
        print("No duplicates found.")
        return
    
    display_options()

    user_input = input("Enter (Y/N): ")

    if user_input.upper() == "Y":
        remove_objects_use_case.execute(bucket_name=aws_bucket_name, resourcesKey=duplicateFiles)
    else:
        return

if __name__ == "__main__":
    main()