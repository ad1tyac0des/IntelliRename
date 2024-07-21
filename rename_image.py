import os
import image_name_generator
from PIL import Image
import uuid
import re
from pillow_avif import AvifImagePlugin
from colorama import init, Fore, Back, Style
import io

# Initialize colorama
init(autoreset=True)

def print_header(message):
    print("\n" + "=" * 50)
    print(f"  {message}")
    print("=" * 50)

def print_step(step_num, message):
    print(f"\n[Step {step_num}] {message}")
    print("-" * 40)

def get_image_format(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format.lower()
    except Exception as e:
        print(f"  {Fore.RED}Error: Unable to detect format of '{image_path}'")
        print(f"  Reason: {str(e)}{Style.RESET_ALL}")
        return None

def convert_to_jpg(image_path):
    try:
        with Image.open(image_path) as img:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            new_filename = f"{base_name}_{uuid.uuid4().hex[:8]}.jpg"
            new_path = os.path.join(os.path.dirname(image_path), new_filename)
            
            # Convert to RGB (this will work for AVIF, WebP and other formats)
            img = img.convert('RGB')
            img.save(new_path, 'JPEG')
        
        print(f"  Converted '{image_path}' to JPEG")
        return new_path
    except Exception as e:
        print(f"  {Fore.RED}Error: Unable to convert '{image_path}' to JPEG")
        print(f"  Reason: {str(e)}{Style.RESET_ALL}")
        return None

def is_three_word_name(filename):
    # Remove file extension
    name_without_extension = os.path.splitext(filename)[0]
    
    # Check if the name matches the pattern of three capitalized words
    pattern = r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$'
    return bool(re.match(pattern, name_without_extension))

def sanitize_filename(filename):
    # Remove or replace characters that are invalid in Windows filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Ensure the filename doesn't start or end with a space or period
    return sanitized.strip('. ')

def create_compressed_copy(image_path, max_size=900*1024):
    with Image.open(image_path) as img:
        # Convert to RGB mode
        img = img.convert('RGB')
        
        # Start with original size
        width, height = img.size
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr = img_byte_arr.getvalue()

        # If image is already small enough, return the original path
        if len(img_byte_arr) <= max_size:
            return image_path

        # If not, start compressing
        scale = 1.0
        quality = 95
        while len(img_byte_arr) > max_size:
            if quality > 30:
                quality -= 5
            else:
                scale *= 0.9
            new_size = (int(width * scale), int(height * scale))
            img_resized = img.resize(new_size, Image.LANCZOS)
            img_byte_arr = io.BytesIO()
            img_resized.save(img_byte_arr, format='JPEG', quality=quality)
            img_byte_arr = img_byte_arr.getvalue()

        # Save compressed image to a temporary file
        temp_path = f"{image_path}_temp.jpg"
        with open(temp_path, 'wb') as f:
            f.write(img_byte_arr)
        print(f"  Created compressed copy: {len(img_byte_arr) / 1024:.2f}KB")
        return temp_path

def generate_valid_name(image_path, max_attempts=5):
    original_path = image_path
    compressed_path = None
    for _ in range(max_attempts):
        try:
            compressed_path = create_compressed_copy(image_path)
            new_name = image_name_generator.generate_image_name(compressed_path)
            sanitized_name = sanitize_filename(new_name)
            if sanitized_name:
                if compressed_path != original_path:
                    os.remove(compressed_path)
                return sanitized_name
        except Exception as e:
            print(f"   Error generating name: {str(e)}")
            print("   Retrying...")
        finally:
            if compressed_path and compressed_path != original_path and os.path.exists(compressed_path):
                os.remove(compressed_path)
    return None

def rename_images(folder_path):
    api_supported_formats = {'jpg', 'jpeg', 'png'}
    convertible_formats = {'gif', 'bmp', 'tiff', 'webp', 'avif'}
    
    print_header(f"{Fore.BLUE}Image Renaming Process Started{Style.RESET_ALL}")
    
    total_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    processed_files = 0
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue
        
        processed_files += 1
        print_step(processed_files, f"Processing '{filename}' {Back.BLUE}{Fore.WHITE}({processed_files}/{total_files}){Style.RESET_ALL}")
        
        if is_three_word_name(filename):
            print(f"  {Fore.YELLOW}Skipped: File already has the correct 3-word format{Style.RESET_ALL}")
            continue
        
        actual_format = get_image_format(file_path)
        if not actual_format:
            continue
        
        converted_file = None
        if actual_format in api_supported_formats:
            process_image = file_path
        elif actual_format in convertible_formats:
            converted_file = convert_to_jpg(file_path)
            if not converted_file:
                continue
            process_image = converted_file
        else:
            print(f"  {Fore.YELLOW}Skipped: Unsupported format '{actual_format}'{Style.RESET_ALL}")
            continue
        
        new_name = generate_valid_name(process_image)
        if not new_name:
            print(f"  {Fore.RED}Error: Unable to generate a valid name for '{filename}'{Style.RESET_ALL}")
            if converted_file:
                os.remove(converted_file)
                print(f"  Removed temporary converted file '{converted_file}'")
            continue
        
        new_extension = '.jpg' if process_image != file_path else os.path.splitext(filename)[1]
        new_filename = f"{new_name}{new_extension}"
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Ensure we don't overwrite existing files
        counter = 1
        while os.path.exists(new_file_path):
            new_filename = f"{new_name}_{counter}{new_extension}"
            new_file_path = os.path.join(folder_path, new_filename)
            counter += 1
        
        try:
            os.rename(process_image, new_file_path)
            print(f"  {Fore.GREEN}Success: Renamed to '{new_filename}'{Style.RESET_ALL}")
            
            if converted_file:
                os.remove(file_path)
                print(f"  Removed original file '{filename}'")
        except Exception as e:
            print(f"  {Fore.RED}Error: Unable to rename '{filename}'")
            print(f"  Reason: {str(e)}{Style.RESET_ALL}")
            if converted_file:
                os.remove(converted_file)
                print(f"  Removed temporary converted file '{converted_file}'")

if __name__ == "__main__":
    folder_path = input("Enter Path to the folder containing the images: ")
    rename_images(folder_path)
    print_header(f"{Fore.GREEN}Image Renaming Process Completed.")