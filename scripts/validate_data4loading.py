import json
from pathlib import Path
from rich import print, inspect

people_records_prepped_file = Path("data/people/people_records_prepped.json")
books2people_prepped_file = Path("data/people/books2people_prepped.json")
folder_matched = Path("data/matched")

validation_log_file = Path("data/logs/validation_failed_log.json")

def create_lookup_structures():
    people_records = []
    books2people_records = []

    with open(people_records_prepped_file, "r") as f:
        people_records = json.load(f)

    with open(books2people_prepped_file, "r") as f:
        books2people_records = json.load(f)

    books2people_dict = {entry["composite_id"]: entry for entry in books2people_records}
    people_dict = {person["unified_id"]: person for person in people_records}

create_lookup_structures()

def validate_data():
    pass
