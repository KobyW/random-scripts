# bulk-remove-rename.py

import os
import re
import subprocess

def main():
    directory = input("Enter the directory to search: ")
    pattern = input("Enter the pattern to remove: ")
    replacement = input("Enter the replacement pattern (or leave empty for removal): ")
    confirm = input(f"Are you sure you want to remove '{pattern}' and replace with '{replacement}' in all files in '{directory}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if pattern in file:
                new_name = file.replace(pattern, replacement)
                os.rename(os.path.join(root, file), os.path.join(root, new_name))

if __name__ == "__main__":
    main()
