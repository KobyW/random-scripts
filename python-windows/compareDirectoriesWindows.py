import os
import subprocess

def open_file_explorer_and_get_path():
    """Open a file explorer window and get the path selected by the user."""
    # Using PowerShell to open the folder dialog and get the folder path
    ps_script = """
    Add-Type -AssemblyName System.windows.forms
    $folder_browser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folder_browser.ShowDialog() | Out-Null
    $folder_browser.SelectedPath
    """

    folder_path = subprocess.check_output(["powershell", "-Command", ps_script]).decode().strip()
    return folder_path

def compare_folders(folder1, folder2):
    """Compare the contents of two folders and print the differences."""
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # Files that are in folder1 but not in folder2
    diff1 = files1 - files2

    # Files that are in folder2 but not in folder1
    diff2 = files2 - files1

    return diff1, diff2

if __name__ == "__main__":
    print("Select the first folder:")
    folder1 = open_file_explorer_and_get_path()

    print("Select the second folder:")
    folder2 = open_file_explorer_and_get_path()

    diff1, diff2 = compare_folders(folder1, folder2)

    if diff1:
        print(f"\nFiles in '{folder1}' but not in '{folder2}':")
        for file in diff1:
            print(file)

    if diff2:
        print(f"\nFiles in '{folder2}' but not in '{folder1}':")
        for file in diff2:
            print(file)

    if not diff1 and not diff2:
        print("\nBoth folders have the same files.")

