import json
import re
from pathlib import Path

people_file = Path("data/processing/people_prepped.json")

def remove_oops():
    with open(people_file, "r") as f:
        people_entries = json.load(f)

        corrupt_keys = {"unified_id", "_source_custom_id", "_error", "_raw_content"}
        cleaned_entries = [entry for entry in people_entries if set(entry.keys()) != corrupt_keys]
    with open(people_file, "w") as f:
        json.dump(cleaned_entries, f, ensure_ascii=False, indent=2)
    print(f"Removed {len(people_entries) - len(cleaned_entries)} corrupt entries")
    print(f"Kept {len(cleaned_entries)} valid entries")
remove_oops()
