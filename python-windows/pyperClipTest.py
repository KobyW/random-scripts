import pyperclip
import time
import requests
import os
import re

def is_valid_url(url, file_extension):
    print(f"Checking URL: {url}")
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code != 200:
            print(f"Invalid status code: {response.status_code}")
            return False
        if f".{file_extension.lower()}?v=" not in url.lower():
            print(f"URL does not contain .{file_extension}?v=")
            return False
        return True
    except Exception as e:
        print(f"Error checking URL: {str(e)}")
        return False


def extract_filename(url, file_extension):
    print(f"Extracting filename from URL: {url}")
    try:
        pattern = rf"products/(.*).{file_extension}\?v="
        filename = re.search(pattern, url).group(1)
        print(f"Extracted filename: {filename}")
        return filename
    except AttributeError:
        print("Failed to extract filename.")
        return None

def download_file(url, save_path, file_extension):
    print(f"Attempting to download file from URL: {url}")
    try:
        file_name = extract_filename(url, file_extension)
        if file_name:
            response = requests.get(url)
            if response.status_code == 200:
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

save_dir = input("Enter the directory to save the files: ")
file_extension = input("Enter the expected file extension (e.g., png, jpg): ")

os.makedirs(save_dir, exist_ok=True)

print("Script is active and running...")
print("Monitoring clipboard for image URLs...")

prev_clipboard_content = pyperclip.paste()

while True:
    try:
        clipboard_content = pyperclip.paste().strip().replace("\n", "").replace("\r", "")
        if (clipboard_content != prev_clipboard_content and 
                is_valid_url(clipboard_content, file_extension)):
            download_file(clipboard_content, save_dir, file_extension)
        prev_clipboard_content = clipboard_content
        time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")
        break
    except Exception as e:
        print(f"Error: {str(e)}")
        time.sleep(5)


