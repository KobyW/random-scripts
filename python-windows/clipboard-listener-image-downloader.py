## Shopify Clipboard Image Downloader
## Koby Wood, Kocanon IT Consulting
## koby@kocanon.com

import pyperclip
import time
import requests
import os
import re

# Function to validate if the URL is valid and accessible
def is_valid_url(url, file_extension):
    print(f"Checking URL: {url}")
    try:
        # Sending a HEAD request to see if the URL is accessible
        response = requests.head(url, allow_redirects=True)
        # Check if response code is 200 OK
        if response.status_code != 200:
            print(f"Invalid status code: {response.status_code}")
            return False
        # Check if the URL has the expected file extension pattern
        if f".{file_extension.lower()}?v=" not in url.lower():
            print(f"URL does not contain .{file_extension}?v=")
            return False
        return True
    except Exception as e:
        print(f"Error checking URL: {str(e)}")
        return False

# Function to extract the filename from the URL
def extract_filename(url, file_extension):
    print(f"Extracting filename from URL: {url}")
    try:
        # Regular expression pattern to extract the filename
        pattern = rf"products/(.*).{file_extension}\?v="
        filename = re.search(pattern, url).group(1)
        print(f"Extracted filename: {filename}")
        return filename
    except AttributeError:
        print("Failed to extract filename.")
        return None

# Function to download a file from a URL and save it to a directory
def download_file(url, save_path, file_extension):
    print(f"Attempting to download file from URL: {url}")
    try:
        # Extracting filename from the URL
        file_name = extract_filename(url, file_extension)
        if file_name:
            # Sending a GET request to download the file
            response = requests.get(url)
            if response.status_code == 200:
                # Constructing the file path and writing the file
                file_path = os.path.join(save_path, f"{file_name}.{file_extension}")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"File downloaded: {file_path}")
            else:
                print(f"Failed to download file: {url}")
        else:
            print(f"Filename could not be extracted from URL: {url}")
    except Exception as e:
        print(f"Error: {str(e)}")

# User input for save directory and file extension
save_dir = input("Enter the directory to save the files: ")
file_extension = input("Enter the expected file extension (e.g., png, jpg): ")

# Creating the save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

print("Script is active and running...")
print("Monitoring clipboard for image URLs...")

# Storing the initial clipboard content
prev_clipboard_content = pyperclip.paste()

# Main loop to monitor the clipboard and download files
while True:
    try:
        # Getting the current clipboard content and stripping newlines and whitespaces
        clipboard_content = pyperclip.paste().strip().replace("\n", "").replace("\r", "")
        # If the clipboard content has changed and it's a valid URL, download the file
        if (clipboard_content != prev_clipboard_content and 
                is_valid_url(clipboard_content, file_extension)):
            download_file(clipboard_content, save_dir, file_extension)
        # Updating the previous clipboard content
        prev_clipboard_content = clipboard_content
        # Waiting for a short period to prevent excessive CPU usage
        time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")
        break
    except Exception as e:
        print(f"Error: {str(e)}")
        time.sleep(5)
