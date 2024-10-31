import csv
import os
import re
import requests

def extract_filename(url):
    try:
        pattern = rf"products/(.*?)\?v="
        filename = re.search(pattern, url).group(1)
        return filename
    except AttributeError:
        return None

def download_file(url, save_path):
    try:
        file_name = extract_filename(url)
        if file_name:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(save_path, file_name)
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
csv_path_user = input("Enter the path to the CSV file: ")

os.makedirs(save_dir, exist_ok=True)

print("Script started...")

try:
    print("Starting to read the CSV file...")
    with open(csv_path_user, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print("Reading a row from the CSV file...")
            img_src = row.get("Image Src")
            if img_src:
                print(f"Attempting to download from URL: {img_src}")
                download_file(img_src, save_dir)
except FileNotFoundError:
    print("The specified CSV file could not be found. Please check the path and try again.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
