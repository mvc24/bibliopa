from docx import Document
import csv
import os

folder_preise = "data/original/preise"
folder_keinepreise = "data/original/keine preise"
files_info = "data/files_info.csv"

def get_file_infos ():
    with open(files_info, "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        rows = list(csv_reader)
        for row in rows:
            filename = row[0]
            row[1] = count_entries(filename, folder_preise)
            # print(f"{filename} has {row[1]} entries with prices")
            row[2] = count_entries(filename, folder_keinepreise)
            # print(f"{filename} has {row[2]} entries without prices")
    with open(files_info, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        csv_writer.writerows(rows)

    print(f"Success!")

# print(files_info_path)

def count_entries(filename, folder_path):
    full_path = folder_path + "/" + filename
    if not os.path.exists(full_path):
        print(f"! File {filename} is missing in {folder_path}")
        return -1
    doc = Document(full_path)
    entries = 0
    for table in doc.tables:
        for row in table.rows:
            if len(row.cells[0].text) >= 2:
                entries += 1

    return entries


get_file_infos()
# count_entries("INSEL-BÜCHEREI.docx", folder_keinepreise)
