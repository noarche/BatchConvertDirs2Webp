import os
import cv2  # OpenCV for image processing
from tqdm import tqdm
import colorama
from colorama import Fore, init

# Initialize colorama for colorful output
init(autoreset=True)

def format_size(bytes_size):
    """Converts bytes to KB, MB, GB, or TB."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def resize_image(img_path, scale_percent):
    """Resizes the image by a given percentage."""
    try:
        # Read the image using OpenCV
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        if img is None:
            raise ValueError(f"Unable to read image: {img_path}")

        # Calculate new dimensions
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        new_dim = (width, height)

        # Resize the image with high-quality interpolation
        resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_CUBIC)

        # Save the resized image
        output_path = f"{os.path.splitext(img_path)[0]}_resized{os.path.splitext(img_path)[1]}"
        cv2.imwrite(output_path, resized_img)
        return img_path, output_path
    except Exception as e:
        print(f"{Fore.RED}Error resizing {img_path}: {e}")
        return None, None

def process_directory(directory, scale_percent):
    total_files = 0
    processed_files = 0
    ignored_files = 0

    for root, dirs, files in os.walk(directory):
        image_files = [f for f in files if f.lower().endswith(('.jpeg', '.jpg', '.png', '.webp'))]

        if not image_files:
            continue

        total_files += len(image_files)

        with tqdm(total=len(image_files), desc=f"Processing in {root}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
            for image_file in image_files:
                img_path = os.path.join(root, image_file)
                orig_path, resized_path = resize_image(img_path, scale_percent)
                if orig_path and resized_path:
                    processed_files += 1
                else:
                    ignored_files += 1

                pbar.update(1)

    print(f"{Fore.GREEN}Image resizing complete!")
    print(f"{Fore.CYAN}Total detected: {total_files}")
    print(f"{Fore.CYAN}Total processed: {processed_files}")
    print(f"{Fore.CYAN}Total ignored: {ignored_files}")

def display_help():
    print(f"{Fore.MAGENTA}This script resizes images by a percentage.")
    print(f"It processes all subdirectories in the provided directory, resizes images, and saves them with '_resized' appended to the filename.")
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

        try:
            scale_percent = float(input(f"{Fore.CYAN}Enter resize percentage (e.g., 50 for 50%): ").strip())
            if scale_percent <= 0:
                print(f"{Fore.RED}Invalid percentage. Please enter a positive number.")
                continue
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")
            continue

        process_directory(directory, scale_percent)

if __name__ == "__main__":
    main()

