import argparse
import subprocess

def run_image_optimization():
    subprocess.run(["python3", "src/image_optimization/main.py"])

def run_find_duplicate():
    subprocess.run(["python3", "src/find_duplicates/main.py"])

def main():
    parser = argparse.ArgumentParser(description="CLI Menu for Image Optimization and Find Duplicate Scripts")
    parser.add_argument("option", choices=["1", "2"], help="Choose an option (1: Image Optimization, 2: Find Duplicate)")

    user_input = input("Enter the option number (1 or 2): ")

    if user_input == "1":
        run_image_optimization()
    elif user_input == "2":
        run_find_duplicate()
    else:
        print("Invalid option. Please enter either '1' or '2'.")

if __name__ == "__main__":
    print("Select an option:")
    print("1. Image Optimization")
    print("2. Find Duplicate")

    main()