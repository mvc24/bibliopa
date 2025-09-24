from pathlib import Path
import json
from scripts.data_prep import consolidate_entries
from pprint import pp

path = Path("data/file_groups.json")

with open(path, "r") as f:
    file_groups = json.load(f)

xl = file_groups["xl"]
# l = file_groups["l"]
# m = file_groups["m"]
# xs = file_groups["xs"]
# s = file_groups["s"]

for file in xl:
    filename = file["filename"]
    consolidate_entries(filename)

# consolidate_entries("ÄGYPTEN VORDERER ORIENT.docx")
