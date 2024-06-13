import os
import sys
import time
from PIL import Image
from pillow_heif import register_heif_opener

# PyInstaller specific imports for handling PIL hidden imports
#use pyinstaller -F python_file.py

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Register HEIF opener for Pillow
register_heif_opener()

def convert_heic(input_folder, custom_name, format, quality=95):
    output_folder = os.path.join(input_folder, format)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_number = 1
    image_count = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            file_path = os.path.join(input_folder, filename)
            try:
                with Image.open(file_path) as img:
                    new_file_name = f"{custom_name}_{file_number:02}.{format}"
                    new_file_path = os.path.join(output_folder, new_file_name)
                    if format == 'jpg':
                        img = img.convert("RGB")
                        img.save(new_file_path, "JPEG", quality=quality)
                    elif format == 'png':
                        img.save(new_file_path, "PNG")
                    print(f"'{new_file_name}' saved to folder: '{format}'")
                    file_number += 1
                    image_count += 1
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
    print(f"Total images processed: {image_count}")

def exit_or_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'exit':
        for i in range(2, 0, -1):
            print(f'Program exited by user. Closing in {i}....')
            time.sleep(1)
        exit()
    return user_input

def main():
    if hasattr(sys, 'frozen'):
        os.chdir(sys._MEIPASS)
    while True:
        print("I AM HEIC CONVERTER. Enter 'exit' to quit")
        while True:
            input_folder = exit_or_input("Enter the input folder path: ")
            if os.path.isdir(input_folder):
                break
            else:
                print("Invalid folder path. Please try again.")
        while True:
            custom_name = exit_or_input("Enter the File name: 'xxx'_ord.format: ")
            if custom_name.isalnum():
                break
            else:
                print("Letters and numbers only. Please try again.")

        while True:
            format = exit_or_input("Enter the output format 'jpg' or 'png': ").lower()
            if format in ['jpg', 'png']:
                break
            else:
                print("Invalid format. Please enter 'jpg' or 'png'.")

        while True:
            proceed = exit_or_input("Enter 'y' to start conversion: ").lower()
            if proceed == 'y':
                convert_heic(input_folder, custom_name, format)
                print("Conversion completed successfully!")
                break
            else:
                print("Invalid command. Please enter 'y' or 'exit'")

if __name__ == "__main__":
    main()