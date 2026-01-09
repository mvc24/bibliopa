import json
import sys

from pathlib import Path


people_file = Path("database/in_progress/people_prepped.json")
# people_file = Path("../in_progress/test_names.json")
people_grouped_file = Path("database/in_progress/people_grouped.json")

def create_people_lookup():
    people_dict = {}
    people_entries = []

    with open(people_file, "r") as f:
        people_entries = json.load(f)
        # print(people_entries)

    for entry in people_entries:
        unified_id = entry["unified_id"]
        people_dict.setdefault(unified_id, []).append(entry)

    sorted_entries = sorted(people_dict.items())
    sorted_dict = dict(sorted_entries)
    # print(sorted_dict)
    with open(people_grouped_file, "w") as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=2)

# create_people_lookup()


# def score_name_info():
