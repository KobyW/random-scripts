#create a csv list of filenames in a directory
#prompt user for directory
#prompt user for output filename
#run through all files in the directory, and add them to a csv list with the filename and path

import os
import csv

def main():
    directory = input("Enter the directory to search: ")
    output_filename = input("Enter the output filename: ")

    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Path'])

        for root, _, files in os.walk(directory):
            for file in files:
                csvwriter.writerow([file, os.path.join(root, file)])

if __name__ == "__main__":
    main()

