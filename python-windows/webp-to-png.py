from PIL import Image
import os
from pathlib import Path
import logging
from typing import List

def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_image_files(directory: str) -> List[Path]:
    """Get all image files in directory excluding PNGs."""
    # Common image extensions
    image_extensions = {'.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
    
    directory_path = Path(directory)
    image_files = []
    
    for file_path in directory_path.iterdir():
        if file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return image_files

def convert_to_png(file_path: Path) -> bool:
    """Convert a single image to PNG format."""
    try:
        with Image.open(file_path) as img:
            # Convert RGBA images to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Create new filename with .png extension
            output_path = file_path.with_suffix('.png')
            img.save(output_path, 'PNG')
            logging.info(f'Successfully converted: {file_path}')
            return True
            
    except Exception as e:
        logging.error(f'Failed to convert {file_path}: {str(e)}')
        return False

def main():
    # Set up logging
    setup_logging()
    
    # Get directory path from user
    directory = input("Enter the directory path containing images: ").strip()
    
    # Validate directory
    if not os.path.isdir(directory):
        logging.error("Invalid directory path!")
        return
    
    # Get list of image files
    image_files = get_image_files(directory)
    
    if not image_files:
        logging.info("No compatible image files found in directory.")
        return
    
    # Convert each image
    successful = 0
    failed = 0
    
    for file_path in image_files:
        if convert_to_png(file_path):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    logging.info(f"\nConversion complete!")
    logging.info(f"Successfully converted: {successful}")
    logging.info(f"Failed conversions: {failed}")

if __name__ == "__main__":
    main()