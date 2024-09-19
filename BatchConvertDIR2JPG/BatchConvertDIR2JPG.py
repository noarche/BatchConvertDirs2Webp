import os
from PIL import Image
from tqdm import tqdm
import colorama
from colorama import Fore, Style, init

# Initialize colorama for colorful output
init(autoreset=True)

def format_size(bytes_size):
    """Converts bytes to KB, MB, GB, or TB."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def convert_image_to_jpg(img_path, quality=100):
    try:
        original_size = os.path.getsize(img_path)
        img = Image.open(img_path)
        img = img.convert("RGB")  # Ensure proper conversion to JPG

        # Define the new file path for the jpg image
        jpg_path = f"{os.path.splitext(img_path)[0]}1.jpg"

        # Save the image as .jpg format with the specified quality
        img.save(jpg_path, 'JPEG', quality=quality)

        # Return paths and sizes
        return img_path, jpg_path, original_size
    except Exception as e:
        print(f"{Fore.RED}Error converting {img_path}: {e}")
        return None, None, None

def process_directory(directory, quality=100):
    total_files = 0
    converted_files = 0
    ignored_files = 0
    total_space_saved = 0

    to_delete = []
    to_rename = []

    for root, dirs, files in os.walk(directory):
        image_files = [f for f in files if f.lower().endswith('.webp')]

        # Skip directory if no valid images are found
        if not image_files:
            continue

        total_files += len(image_files)

        # Convert images from WebP to JPG
        with tqdm(total=len(image_files), desc=f"Converting in {root}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
            for image_file in image_files:
                img_path = os.path.join(root, image_file)
                orig_path, jpg_path, original_size = convert_image_to_jpg(img_path, quality)
                if orig_path and jpg_path:
                    converted_files += 1
                    new_size = os.path.getsize(jpg_path)
                    total_space_saved += original_size - new_size

                    # Track files for deletion and renaming
                    to_delete.append(orig_path)
                    to_rename.append((jpg_path, orig_path))  # Rename 'jpg_path' to 'orig_path' after deletion

                pbar.update(1)

            ignored_files += 0  # As we are converting all webp files, no files are ignored

    # Second Task: Delete original WebP files
    print(f"{Fore.YELLOW}Deleting original WebP files...")
    for file_path in to_delete:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"{Fore.RED}Error deleting {file_path}: {e}")

    print(f"{Fore.GREEN}Conversion complete!")
    print(f"{Fore.CYAN}Total detected: {total_files}")
    print(f"{Fore.CYAN}Total converted: {converted_files}")
    print(f"{Fore.CYAN}Total ignored: {ignored_files}")
    print(f"{Fore.CYAN}Total space saved: {format_size(total_space_saved)}")
    print(f"{Fore.YELLOW}Build Date: SEPTEMBER 19 2024")
    print(f"{Fore.YELLOW}Version: 0.0.1.8")
    print(f"{Fore.BLUE}Thanks for using BatchConvertDIR2JPG by noarche!")
    print(f"{Fore.BLUE}https://github.com/noarche")

def display_help():
    print(f"{Fore.MAGENTA}This script converts .webp images to .jpg format.")
    print("It processes all subdirectories in the provided directory, converting and renaming files.")
    print(f"If the image is already in .jpg format, it will be ignored.")
    print(f"Type 'exit' or 'e' to quit the program.")

def main():
    while True:
        directory = input(f"{Fore.CYAN}Enter directory or type 'help' for more information: ").strip()

        if directory.lower() in ['exit', 'e']:
            print(f"{Fore.YELLOW}Exiting program.")
            break

        if directory.lower() == 'help':
            display_help()
            continue

        if not os.path.isdir(directory):
            print(f"{Fore.RED}Invalid directory. Please try again.")
            continue

        # Ask for compression quality with a default of 100
        quality_input = input(f"{Fore.CYAN}Enter JPG quality (1-100, default is 100): ").strip()
        if quality_input.isdigit():
            quality = int(quality_input)
        else:
            quality = 100

        process_directory(directory, quality)

if __name__ == "__main__":
    main()
