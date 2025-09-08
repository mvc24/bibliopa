from docx import Document
import csv
import os
import re


folder_preise = "data/original/preise/"
folder_keinepreise = "data/original/keine preise/"
files_info = "data/files_info_header.csv"

def get_entries(filename, folder_path):
    full_path = folder_path + filename
    entries = []
    if not os.path.exists(full_path):
        print(f"! File {filename} is missing in {folder_path}")
        return -1
    doc = Document(full_path)
    count = 0
    for table in doc.tables:
        for row in table.rows:
            if len(row.cells[0].text) >= 2:
                count += 1
                price_removed = re.sub(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", "", row.cells[0].text)
                entries.append({"text": price_removed, "source": full_path})
    print(entries)

get_entries("ZEITSCHRIFTEN.docx", folder_preise)
