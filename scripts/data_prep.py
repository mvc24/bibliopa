from docx import Document
import csv
import os
import re
from pprint import pp


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

def consolidate_entries(filename):
    paths = {
        'p': folder_preise + filename,
        'kp': folder_keinepreise + filename
    }
    entries = {}

    # read & process each file
    for version, path in paths.items():
        # print(f"Current version: {version}")
        # print(f"Current path: {path}")
        # print(f"Full paths dict: {paths}")
        entries[version] = []
        if not os.path.exists(path):
            print(f"! File {path} does not exist")
            return -1
        doc = Document(path)
        count = 0
        for table in doc.tables:
            for row in table.rows:
                if len(row.cells[0].text) >= 2:
                    count += 1
                    price_removed = re.sub(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", "", row.cells[0].text)
                    entries[version].append({"text": price_removed, "source": version + "-" + filename})
    pp(entries["p"][17])


consolidate_entries("ZEITSCHRIFTEN.docx")

# get_entries("ZEITSCHRIFTEN.docx", folder_preise)
