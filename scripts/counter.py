from docx import Document
import csv
import os

folder_preise = "data/original/preise"
folder_keinepreise = "data/original/keine preise"
files_info = "data/files_info.csv"

def get_file_infos ():
    with open(files_info, "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        line_count = 0
        for row in csv_reader:
            filename = row[0]
            line_count += 1
            print(row[0])
    print(f"Processed {line_count} lines.")

# print(files_info_path)
# get_file_infos()

def count_entries(filename, folder_path):
    full_path = folder_path + "/" + filename
    doc = Document(full_path)
    entries = 0
    for table in doc.tables:
        for row in table.rows:
            if len(row.cells[0].text) >= 2:
                entries += 1
    print(f"{filename} has {entries} entries.")
    return entries


count_entries("INSEL-BÜCHEREI.docx", folder_keinepreise)
