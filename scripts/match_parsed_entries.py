from rich import print as rprint
from rich import inspect
import json
import re
from datetime import datetime
from pathlib import Path
from text_matching import test_similarity, normalise_text
from progress import progress

folder_prepped = Path("data/raw/prepped")
folder_parsed = Path("data/parsed")

def match_prepped2parsed():
    lookup_dict = {}
    try:
        for file in folder_parsed.iterdir():
            with open(file, "r") as f:
                entries_parsed = json.load(f)

            for entry in entries_parsed:
                key = normalise_text(entry["parsed_entry"]["administrative"]["original_entry"])
                lookup_dict[key] = entry
                lookup_dict.update({key: entry for entry in entries_parsed})

        print(f"Number of entries in parsed file: {len(entries_parsed)}")
        print(f"Number of entries in lookup_dict: {len(lookup_dict)}")

    except json.JSONDecodeError as e:
        rprint(f"Something went wrong: {e}")

    for file in folder_prepped.iterdir():
        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist")

        with open(file, "r") as f:
            entries = json.load(f)
            matched_count = 0
            unmatched_count = 0

        for entry in entries:

            text = entry["text"]
            if text.startswith("AUS!"):
                # rprint("Found one!")
                continue
            text_norm = normalise_text(text)
            topic = entry["topic"]
            price = entry["price"]


            if text_norm in lookup_dict:
                matched_count += 1
                # parsed_entry = lookup_dict[text]
                # parsed_topic = parsed_entry["parsed_entry"]["topic"]
                # parsed_price = parsed_entry["parsed_entry"]["price"]

            else:
                unmatched_count += 1

    rprint(f"\n=== RESULTS ===")
    rprint(f"Matches found: {matched_count}")
    rprint(f"No matches found: {unmatched_count}")


match_prepped2parsed()
