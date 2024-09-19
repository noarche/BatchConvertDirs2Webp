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

def remove_image_metadata(img_path):
    try:
        original_size = os.path.getsize(img_path)
        img = Image.open(img_path)
        img = img.convert("RGB")  # Remove any alpha channels and ensure compatibility
        
        # Define the new file path for the image without metadata
        output_path = f"{os.path.splitext(img_path)[0]}_nometa{os.path.splitext(img_path)[1]}"

        # Save the image without any metadata
        img.save(output_path, quality=100)

        # Return paths and sizes
        return img_path, output_path, original_size
    except Exception as e:
        print(f"{Fore.RED}Error processing {img_path}: {e}")
        return None, None, None

def process_directory(directory):
    total_files = 0
    processed_files = 0
    ignored_files = 0
    total_space_saved = 0

    to_delete = []
    to_rename = []

    for root, dirs, files in os.walk(directory):
        # Include all relevant image file formats
        image_files = [f for f in files if f.lower().endswith(('.jpeg', '.jpg', '.png', '.webp'))]

        # Skip directory if no valid images are found
        if not image_files:
            continue

        total_files += len(image_files)

        # Remove metadata from each image
        with tqdm(total=len(image_files), desc=f"Processing in {root}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
            for image_file in image_files:
                img_path = os.path.join(root, image_file)
                orig_path, nometa_path, original_size = remove_image_metadata(img_path)
                if orig_path and nometa_path:
                    processed_files += 1
                    new_size = os.path.getsize(nometa_path)
                    total_space_saved += original_size - new_size

                    # Track files for deletion and renaming
                    to_delete.append(orig_path)
                    to_rename.append((nometa_path, orig_path))  # Rename '_nometa' file to original after deletion

                pbar.update(1)

    # Second Task: Delete original image files (with metadata)
    print(f"{Fore.YELLOW}Deleting original files...")
    for file_path in to_delete:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"{Fore.RED}Error deleting {file_path}: {e}")

    # Rename the metadata-free files back to their original names
    for old_path, new_path in to_rename:
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"{Fore.RED}Error renaming {old_path} to {new_path}: {e}")

    print(f"{Fore.GREEN}Metadata removal complete!")
    print(f"{Fore.CYAN}Total detected: {total_files}")
    print(f"{Fore.CYAN}Total processed: {processed_files}")
    print(f"{Fore.CYAN}Total ignored: {ignored_files}")
    print(f"{Fore.CYAN}Total space saved: {format_size(total_space_saved)}")
    print(f"{Fore.YELLOW}Build Date: SEPTEMBER 16 2024")
    print(f"{Fore.YELLOW}Version: 0.0.1.9")
    print(f"{Fore.BLUE}Thanks for using BatchRemoveMetadata by noarche!")
    print(f"{Fore.BLUE}https://github.com/noarche")

def display_help():
    print(f"{Fore.MAGENTA}This script removes all metadata from supported image formats (.jpeg, .jpg, .png, .webp).")
    print("It processes all subdirectories in the provided directory, removes metadata, and renames files.")
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

        process_directory(directory)

if __name__ == "__main__":
    main()
