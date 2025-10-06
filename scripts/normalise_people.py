from calendar import c
from rich import print as rprint
from rich import inspect
import json
import re
from datetime import datetime
from pathlib import Path
from text_matching import test_similarity, normalise_text
from progress import progress

# people_file = Path("test_entries.json")
people_file = Path("database/in_progress/collect_people.json")
grouped_people_file = Path("database/in_progress/people_grouped.json")
# grouped_people_file = Path("test_names.json")
wonky_people_file = Path("database/in_progress/wonky_people.json")

org_keywords = ["stiftung", "archiv", "gesellschaft", "forum", "gemeinde", "sammlung", "institut", "museum", "kultur", "kuratorium", "verlag", "ministerium", "akademie", "trust", "verein", "organisation", "vereinigung", "universität", "bibliothek"]

def process_people_smart():
    if not people_file.exists():
        raise FileNotFoundError("collected_people file doesn't exist!")
    if not grouped_people_file.exists():
        raise FileNotFoundError("Grouped file doesn't exist!")

    people_grouped = {}

    with open(people_file, "r") as f:
        collected_people = json.load(f)

        for entry in collected_people:
            is_organisation = False
            family_name = entry["family_name"]
            given_names = entry["given_names"]
            single_name = entry["single_name"]

            name = family_name or None
            if not name or name == "null":
                name = single_name or None
                if not name or name == "null":
                    name = "oops, something went wrong"

            name = normalise_text(name)

            if not given_names or given_names == "null":
                initial = None
            else:
                initial = given_names[0].lower()
                initial = normalise_text(initial)

            if initial:
                name_key = name + "_" + initial
            else:
                name_key = name

            is_org = any(keyword in name_key for keyword in org_keywords)
            if is_org:
                is_organisation = True

            entry["is_organisation"] = is_organisation


            if name_key not in people_grouped:
                people_grouped[name_key] = [entry]
            else:
                people_grouped[name_key].append(entry)

    people_sorted = sorted(people_grouped.items())
    dict(people_sorted)

    try:
        with open(grouped_people_file, "w") as f:
            json.dump(people_sorted, f, ensure_ascii=False, indent=2)

    except json.JSONDecodeError as e:
        print(f"something went awry: {e}")
    # inspect(people_grouped)

    total = len(collected_people)
    grouped = len(people_sorted)

    reduction = ((total - grouped) / total ) * 100


    # print(f"Collected people had {len(collected_people)} entries.")
    # print(f"The grouped file currently has {len(people_sorted)} entries.")
    # print(f"That's a reduction by {reduction:.2f}%, if this math is finally mathing.")

    # inspect(people_grouped)
    return people_sorted

# process_people_smart()

def find_wonky_people_entries():

    people = process_people_smart()
    wonky_entries = {}
    people_without_wonkies = {}

    for name, entries in people:
        if name == "oops, something went wrong":
            wonky_entries[name] = entries
            continue

        und = " und "
        comma = ", "

        for person in entries:
            if (
                (re.search(und, name) or re.search(comma, name)) and
                person["family_name"] is None and
                person["given_names"] is None and
                person["name_particles"] is None and
                person["is_organisation"] is False

            ):
                names_split = re.split(und, name)
                for name in names_split:
                    if name not in wonky_entries:
                        wonky_entries[name] = [entries]
                    else:
                        wonky_entries[name].append(entries)

        try:
            with open(wonky_people_file, "w") as f:
                json.dump(wonky_entries, f, ensure_ascii=False, indent=2)

        except json.JSONDecodeError as e:
            print(f"something went awry: {e}")

#         # if not entries["family_name"] == None or "null"
#         # if und in name or comma in name:
#         #     names_split = re.split(und, name)

#         #     for name in names_split:

#         #         if name not in wonky_entries:
#         #             wonky_entries[name] = [entries]
#         #         else:
#         #             wonky_entries[name].append(entries)

    print(f"{len(wonky_entries)} wonky people were found. ")
    # rprint(wonky_entries)
#     # inspect(wonky_entries)

find_wonky_people_entries()

# def process_people_exact():
#     if not people_file.exists():
#         raise FileNotFoundError("collected_people file doesn't exist!")
#     if not grouped_people_file.exists():
#         raise FileNotFoundError("Grouped file doesn't exist!")

#     people_grouped = {}

#     with open(people_file, "r") as f:
#         collected_people = json.load(f)

#         for entry in collected_people:
#             display_name = entry["display_name"]
#             if not display_name:
#                 display_name = "oops this is no good"
#             name = normalise_text(display_name)

#             if name not in people_grouped:
#                 people_grouped[name] = [entry]
#             else:
#                 people_grouped[name].append(entry)

#     people_sorted = sorted(people_grouped.items())
#     dict(people_sorted)

#     try:
#         with open(grouped_people_file, "w") as f:
#             json.dump(people_sorted, f, ensure_ascii=False, indent=2)

#     except json.JSONDecodeError as e:
#         print(f"something went awry: {e}")
#     # inspect(people_grouped)

#     total = len(collected_people)
#     grouped = len(people_sorted)

#     reduction = ((total - grouped) / total ) * 100


#     # print(f"Collected people had {len(collected_people)} entries.")
#     # print(f"The grouped file currently has {len(people_sorted)} entries.")
#     # print(f"That's a reduction by {reduction:.2f}%, if this math is finally mathing.")

#     return people_sorted
#     inspect(people_grouped)

# process_people_exact()



# def process_people_fuzzy():

#     if not grouped_people_file.exists():
#         raise FileNotFoundError("Grouped file doesn't exist!")

#     return
