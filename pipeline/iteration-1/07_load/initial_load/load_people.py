from rich import print, inspect
import sys
import uuid
import json
import unicodedata
from pathlib import Path
from datetime import datetime

file_path = Path("database/in_progress/pass2_results/results_pass2_002.json")
people_file_path = Path("data/people/people_records_validated.json")
# file_path = Path("database/in_progress/people_results.json")


def load_people():
    with open(people_file_path, "r") as f:
        people = json.load(f)
    people_data = []
    person_id_dict = {}

    for person_id, person in enumerate(people, start=1):
        people_data.append({
            "person_id": person_id,
            "unified_id": person["unified_id"],
            "family_name": person["family_name"],
            "given_names": person["given_names"],
            "name_particles": person["name_particles"],
            "single_name": person["single_name"],
            "is_organisation": person["is_organisation"]
        })
        person_id_dict[person["unified_id"]] = person_id

    # print(people_data)

    return people_data, person_id_dict
#load_people()
