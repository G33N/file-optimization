import os
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.infrastructure.database_repository import DatabaseRepository
from remove_broken_files.application.find_broken_file_path import FindBrokenFilePathUseCase
from remove_broken_files.application.remove_broken_file_path import RemoveBrokenFilePathUseCase
from remove_broken_files.application.check_path_status import CheckPathStatusUseCase


def display_welcome_message():
    print("CLI application developed by G33N for find and remove broken file links!")
    print("-----------------------------------------------------------------")

def display_options():
    print("-----------------------------------------------------------------")
    print("Do you want to find and remove duplicates from your Database?")
    print("-----------------------------------------------------------------")

def get_input(message):
    key = input(message+": ")
    return key


def main():
    display_welcome_message()

    database_repository = DatabaseRepository()

    find_broken_file_path_use_case = FindBrokenFilePathUseCase(database_repository)
    remove_broken_file_path_use_case = RemoveBrokenFilePathUseCase(database_repository)

    files = find_broken_file_path_use_case.execute()

    files_to_process = files

    try:
        check_path_status_use_case = CheckPathStatusUseCase()

        broken_paths = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_file = {executor.submit(check_path_status_use_case.execute, file): file for file in files_to_process}
            
            for future in tqdm(as_completed(future_to_file), total=len(files_to_process), desc="Checking paths", unit="path"):
                future.result()

        broken_paths = check_path_status_use_case.get_broken_paths()
        print("Broken paths:", broken_paths)
    finally:
        database_repository.close()

    if len(broken_paths) == 0:
        print("No broken links found.")
        return
    
    display_options()

    user_input = input("Enter (Y/N): ")

    if user_input.upper() == "Y":
        remove_broken_file_path_use_case.execute(files=broken_paths)
    else:
        return

if __name__ == "__main__":
    main()