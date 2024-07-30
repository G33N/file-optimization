import argparse
import subprocess

def run_image_optimization():
    subprocess.run(["python3", "src/image_optimization/main.py"])

def run_find_duplicate():
    subprocess.run(["python3", "src/find_duplicates/main.py"])

def run_find_borken_file_path():
    subprocess.run(["python3", "src/remove_broken_files/main.py"])

def main():
    parser = argparse.ArgumentParser(description="CLI Menu for Image Optimization and Find Duplicate Scripts")
    parser.add_argument("option", choices=["1", "2"], help="Choose an option (1: Image Optimization, 2: Find Duplicate)")

    user_input = input("Enter the option number: ")

    if user_input == "1":
        run_image_optimization()
    elif user_input == "2":
        run_find_duplicate()
    elif user_input == "3":
        run_find_borken_file_path()
    else:
        print("Invalid option. Please enter a valid option.")

if __name__ == "__main__":
    print("Select an option:")
    print("1. Image Optimization")
    print("2. Find Duplicate")
    print("3. Find Duplicate and remove broken links")

    main()