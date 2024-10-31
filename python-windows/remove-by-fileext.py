import os

def remove_files_by_extension(directory, extension):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                os.remove(os.path.join(root, file))
                count += 1
    return count

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    extension = input("Enter the file extension to remove: ")
    count = remove_files_by_extension(directory, extension)
    print(f"Removed {count} files with extension {extension} from {directory}")
