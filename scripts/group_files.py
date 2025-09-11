import csv
import json
from pathlib import Path
from pprint import pp

file_groups = Path("data/file_groups.json")
groups = {
    "xs": [], # < 60
    "s": [], # < 100
    "m": [], # < 250
    "l": [], # < 499
    "xl": [] # > 500
}

def check_file_size ():
    with open("data/files_info.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        rows = list(csv_reader)
        for row in rows:
            filename = row[0]
            count = int(row[2])
            if count < 60:
                groups["xs"].append({"filename": filename, "count": count})
            elif count < 100:
                groups["s"].append({"filename": filename, "count": count})
            elif count < 250:
                groups["m"].append({"filename": filename, "count": count})
            elif count < 499:
                groups["l"].append({"filename": filename, "count": count})
            elif count >= 500:
                groups["xl"].append({"filename": filename, "count": count})

    if not file_groups.exists():
        raise FileNotFoundError("file_groups file missing!")
    else:
        with open(file_groups, "w") as f:
            json.dump(groups, f, ensure_ascii=False, indent=4)

check_file_size()
