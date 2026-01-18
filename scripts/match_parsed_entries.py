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
folder_matched = Path("data/matched")

def create_lookup():
    corrupt_log_file = Path("data/logs/corrupt_entries_log.json")
    cleaned_file = Path("data/processing/cleaned_corrupt_entries.json")
    lookup_dict = {}

    with open(corrupt_log_file, "r") as f:
        corrupt_log = json.load(f)

    with open(cleaned_file, "r") as f:
        cleaned_entries = json.load(f)

    # Create set of corrupt IDs
    corrupt_ids = {entry["custom_id"] for entry in corrupt_log}

    # Create lookup dict for cleaned entries
    cleaned_dict = {entry["custom_id"]: entry for entry in cleaned_entries}

    for file in folder_parsed.iterdir():

        with open(file, "r") as f:
            entries_parsed = json.load(f)

            for entry in entries_parsed:

                if entry["custom_id"] in corrupt_ids:
                    entry = cleaned_dict[entry["custom_id"]]

                if "parsed_entry" in entry and isinstance(entry["parsed_entry"], list):
                    entry["parsed_entry"] = entry["parsed_entry"][0]

                if "error" in entry or "parsed_entry" not in entry:
                    if entry["custom_id"] not in corrupt_ids:
                        rprint(f"ERROR: Unexpected error in {entry["custom_id"]}")
                    continue

                # DEBUG: Print what we're about to process
                # rprint(f"\nProcessing ID: {entry['custom_id']}")
                # rprint(f"Has 'parsed_entry'? {'parsed_entry' in entry}")
                # rprint(f"Type of entry['parsed_entry']: {type(entry['parsed_entry'])}")


                key = normalise_text(entry["parsed_entry"]["administrative"]["original_entry"])

                lookup_dict[key] = entry
                # lookup_dict.update({key: entry for entry in entries_parsed})

    # rprint(f"Number of entries in parsed file: {len(entries_parsed)}")
    # rprint(f"Number of entries in lookup_dict: {len(lookup_dict)}")
    return lookup_dict


# create_lookup()

def match_prepped2parsed():
    lookup_dict = create_lookup()
    i = 0
    for file in folder_prepped.iterdir():
        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist")

        with open(file, "r") as f:
            entries = json.load(f)
            matched_count = 0
            unmatched_count = 0
            i+=1

        matched_entries = {}
        unmatched_entries = []

        for entry in entries:

            text = entry["text"]
            total_entries = len(entries)
            if text.startswith("AUS!"):
                # rprint("Found one!")
                continue
            text_norm = normalise_text(text)
            topic = entry["topic"]
            price = entry["price"]


            if text_norm in lookup_dict:
                matched_count += 1
            # GET entry
                parsed_entry = lookup_dict[text_norm]
            # Extract values for comparison

                parsed_id = parsed_entry["custom_id"]
                parsed_topic = parsed_entry["parsed_entry"]["topic"]
                parsed_price = parsed_entry["parsed_entry"]["price"]

                if topic == parsed_topic:
                    topic_changed = 0
                else:
                    topic_changed = 1
                    parsed_entry["parsed_entry"]["topic"] = topic

                if price == parsed_price:
                    price_changed = 0
                else:
                    price_changed = 1
                    parsed_entry["parsed_entry"]["price"] = price

                parsed_entry["parsed_entry"]["administrative"]["topic_changed"] = topic_changed
                parsed_entry["parsed_entry"]["administrative"]["price_changed"] = price_changed

            # Store the modified version
                matched_entries[parsed_id] = parsed_entry

            else:
                unmatched_count += 1
                unmatched_entries.append(entry)

    # write results to files
        matched_path = folder_matched / file.name

        with open(matched_path, "w") as f:
            json.dump(matched_entries, f, ensure_ascii=False, indent=2)

        unmatched_file = Path("data/processing/unmatched_entries.json")
        with open(unmatched_file, "r") as f:
            unmatched_list = json.load(f)
            unmatched_list.extend(unmatched_entries)
            unmatched_total = len(unmatched_list)
        with open (unmatched_file, "w") as f:
            json.dump(unmatched_list, f, ensure_ascii=False, indent=2)

        rprint(f"\n=== RESULTS ===")
        rprint(f"{file.name} has {total_entries} entries. {matched_count} were matched, {unmatched_count} remain.")
    rprint(f"{i} files have been processed.")
    rprint(f"There is a total of {unmatched_total} entries.")


match_prepped2parsed()
