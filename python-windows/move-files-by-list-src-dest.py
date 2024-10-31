#prompt user for csv list of filepaths
#prompt user asking if first line is headers
#prompt user for source directory
#prompt user for destination directory
#run through each row of the csv list
#move the file from the source directory to the destination directory
#print out the source and destination filepaths
#print out the number of files moved

import csv
import os
import shutil

def move_files():
    # Get input from user
    csv_path = input("Enter the path to your CSV file: ")
    has_headers = input("Does the CSV have headers? (y/n): ").lower() == 'y'
    
    # Get header column if headers exist
    header_column = 0
    if has_headers:
        with open(csv_path, 'r') as csv_file:
            headers = next(csv.reader(csv_file))
            print("\nAvailable headers:")
            for i, header in enumerate(headers):
                print(f"{i}: {header}")
            header_column = int(input("\nEnter the number of the column containing filenames: "))
    
    source_dir = input("Enter the source directory path: ")
    dest_dir = input("Enter the destination directory path: ")

    # Counter for moved files
    files_moved = 0

    try:
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Skip header row if exists
            if has_headers:
                next(csv_reader)
            
            # Process each row
            for row in csv_reader:
                if not row or len(row) <= header_column:  # Skip empty rows or rows without enough columns
                    continue
                    
                filename = row[header_column]  # Use selected column for filename
                source_path = os.path.join(source_dir, filename)
                dest_path = os.path.join(dest_dir, filename)
                
                # Check if source file exists
                if os.path.exists(source_path):
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    # Move the file
                    shutil.move(source_path, dest_path)
                    print(f"Moved: {source_path} -> {dest_path}")
                    files_moved += 1
                else:
                    print(f"Source file not found: {source_path}")

        print(f"\nTotal files moved: {files_moved}")

    except FileNotFoundError:
        print("Error: CSV file not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    move_files()