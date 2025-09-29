from calendar import c
from rich import print as rprint
from rich import inspect
import json
from datetime import datetime
from pathlib import Path
from text_matching import test_similarity, normalise_text
from progress import progress

people_file = Path("database/in_progress/collect_people.json")
# people_file = Path("test_entries.json")
grouped_people_file = Path("database/in_progress/people_grouped.json")

def process_people_exact():
    if not people_file.exists():
        raise FileNotFoundError("collected_people file doesn't exist!")
    if not grouped_people_file.exists():
        raise FileNotFoundError("Grouped file doesn't exist!")

    people_grouped = {}

    with open(people_file, "r") as f:
        collected_people = json.load(f)

        for entry in collected_people:
            display_name = entry["display_name"]
            if not display_name:
                display_name = "oops this is no good"
            name = normalise_text(display_name)

            if name not in people_grouped:
                people_grouped[name] = [entry]
            else:
                people_grouped[name].append(entry)

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


    print(f"Collected people had {len(collected_people)} entries.")
    print(f"The grouped file currently has {len(people_sorted)} entries.")
    print(f"That's a reduction by {reduction:.2f}%, if this math is finally mathing.")

    return people_sorted
    # inspect(people_grouped)

# process_people_exact()

def process_people_fuzzy():

    return
