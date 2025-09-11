from pathlib import Path
import json
from scripts.data_prep import consolidate_entries
from pprint import pp

path = Path("data/file_groups.json")

with open(path, "r") as f:
    file_groups = json.load(f)

s = file_groups["s"]


for file in s:
    filename = file["filename"]
    consolidate_entries(filename)
