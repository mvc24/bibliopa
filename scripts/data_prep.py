from docx import Document
import csv
import os
import re
from pprint import pp


folder_preise = "data/original/preise/"
folder_keinepreise = "data/original/keine preise/"
files_info = "data/files_info_header.csv"

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

        topic = filename.replace(".docx", "")
        topic_normalized = topic.lower().split()[0]
        topic_normalized = topic_normalized.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        count = 0

        for table in doc.tables:
            for row in table.rows:
                if len(row.cells[0].text) >= 2:
                    count += 1

                    find_price = re.search(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", row.cells[0].text)
                    if find_price:
                        find_price = find_price.group()
                        price_number = re.search(r'\d+', find_price)
                        find_price = int(price_number.group()) if price_number else None
                    else:
                        find_price = None
                    price_removed = re.sub(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", "", row.cells[0].text)

                    text_normalised = price_removed.replace('\n', '. ')
                    text_normalised = ' '.join(text_normalised.split())


                    entries[version].append({
                        "text": text_normalised,
                        "source": version + "-" + filename,
                        "price": find_price,
                        "topic": topic,
                        "topic_normalized": topic_normalized
                        })

    # pp(entries["p"][5], width=150)
    pp(entries["p"][12], width=150)
    pp(entries["kp"][12], width=150)
    # pp(entries["kp"][17], width=150)
    # pp(entries["p"])


consolidate_entries("ÄGYPTEN VORDERER ORIENT.docx")

# get_entries("ZEITSCHRIFTEN.docx", folder_preise)
