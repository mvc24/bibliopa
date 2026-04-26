from docx import Document
from datetime import datetime
import os
from pathlib import Path
import re
import json
from pprint import pp
import unicodedata


folder_preise = "data/original/preise/"
folder_keinepreise = "data/original/keine preise/"
files_info = "data/files_info_header.csv"
discrepancies_file = Path("data/discrepancies.json")
processing_log = Path("data/logs/processing_log.json")

def consolidate_entries(filename):
    paths = {
        'p': folder_preise + filename,
        'kp': folder_keinepreise + filename
    }
    entries = {}

    # read & process both files
    # Loop runs twice: once for 'p', once for 'kp'
    for version, path in paths.items():
        # print(f"Current version: {version}")
        # print(f"Current path: {path}")
        # print(f"Full paths dict: {paths}")
        entries[version] = []
        if not os.path.exists(path):
            print(f"! File {path} does not exist")
            return -1
        doc = Document(path)

        topic = filename.upper().replace(".DOCX", "")
        if topic == "DEUTSCHE LITERATUR MONOGRAPHIEN":
            topic_normalised = "de-lit-monographien"
        elif topic == "DEUTSCHE LITERATUR TEXTE":
            topic_normalised = "de-lit-texte"
        elif topic == "ERSTAUSGABEN A - G":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben1"
        elif topic == "ERSTAUSGABEN H - M":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben2"
        elif topic == "ERSTAUSGABEN N - Z":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben3"
        else:
            topic_lower = topic.lower()
            if "-" in topic_lower:
                topic_normalised = topic_lower.split("-")[0]
            elif "," in topic_lower:
                topic_normalised = topic_lower.split(",")[0]
            else:
                topic_normalised = topic_lower.split()[0]  # Split on spaces, take first word

            topic_normalised = unicodedata.normalize("NFC", topic_normalised)

            topic_normalised = topic_normalised.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')

        count = 0

        for table in doc.tables:
            for row in table.rows:
                if len(row.cells[0].text) >= 2:
                    count += 1

                    find_price = re.search(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", row.cells[0].text)
                    if find_price:
                        find_price = find_price.group()
                        price_number = re.search(r'\d+', find_price)
                        find_price = int(price_number.group()) if price_number else None
                    else:
                        find_price = None
                    price_removed = re.sub(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", "", row.cells[0].text)
                    price_cleaned = re.sub(r"\ba`\s*", "", price_removed)

                    text_normalised = price_cleaned.replace('\n', '. ')
                    text_normalised = ' '.join(text_normalised.split())

                    entries[version].append({
                        "text": text_normalised,
                        "source": version + "-" + filename,
                        "price": find_price,
                        "topic": topic,
                        "topic_normalised": topic_normalised
                        })

        if version == "p":
            count_p = count
        elif version == "kp":
            count_kp = count

    # Files have been processed, content of rows normalised and stored in dictionaries.
    base_entries = entries["kp"]  # Always use kp as authoritative
    match_entries = entries["p"]   # Always try to get prices from p

# TEXT MATCHING STEP:

# TEXT MATCHING LOGIC - DATA SOVEREIGNTY RULES:
#
# PRIMARY SOURCE (kp): Contains the authoritative, most recent data
# - Use for: text content, topic, topic_normalized
# - This is the "master" version with grandfather's latest edits
#
# SECONDARY SOURCE (p): Contains pricing data only
# - Use for: price field only
# - This is the older version that still has prices before they were removed
#
# MATCHING GOAL: Find same entries in both files to combine kp content + p prices
# UNMATCHED kp entries: Keep them (they're still valid, just no price available)
# UNMATCHED p entries: Add to discrepancies (they were removed from kp for a reason)


# 1. Initialize new data collections

    records = []
    p_entries_matched = set()

# 2. Loop through base_entries using enumerate to get both index and entry
# 3. For each base_entry, first try to match at the same index in match_entries
# 4. If same-index match fails, search through all of match_entries
# 7. Handle matches
# 8. Create matched record when match is found

    for index, base_entry in enumerate(base_entries):
        if index < len(match_entries):
            if base_entry["text"].strip() == match_entries[index]["text"].strip():
                p_entries_matched.add(index)
                records.append({
                    "text": base_entry["text"],
                    "price": match_entries[index]["price"],
                    "topic": base_entry["topic"],
                    "topic_normalised": base_entry["topic_normalised"]
                })
            else:
                for search_index, match_entry in enumerate(match_entries):
                    if base_entry["text"].strip() == match_entry["text"].strip():
                        p_entries_matched.add(search_index)
                        records.append({
                            "text": base_entry["text"],
                            "price": match_entry["price"],
                            "topic": base_entry["topic"],
                            "topic_normalised": base_entry["topic_normalised"]
                        })
                        break
                else:
                    records.append({
                            "text": base_entry["text"],
                            "price": None,
                            "topic": base_entry["topic"],
                            "topic_normalised": base_entry["topic_normalised"]
                        })
        else:
            records.append({
                            "text": base_entry["text"],
                            "price": None,
                            "topic": base_entry["topic"],
                            "topic_normalised": base_entry["topic_normalised"]
                        })

# save records to file
#   create filename

    records_file = topic_normalised + ".json"

    path = Path("data/consolidated")
    records_path = path / records_file

    with open(records_path, "w") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

    pp(f"Records successfully saved to {records_path}")


# 5. Add unmatched entries to discrepancies

    p_indices = set(range(len(match_entries)))
    unmatched_indices = p_indices - p_entries_matched

    entries_for_discrepancies = []

    for unmatched_index in unmatched_indices:
        entry = match_entries[unmatched_index]
        entries_for_discrepancies.append(entry)

    # pp(entries_for_discrepancies)

# 6. Write discrepancies into file
    if not discrepancies_file.exists():
        raise FileNotFoundError("discrepancies file missing!")
    else:
        with open(discrepancies_file, "r") as f:
            discrepancy_list = json.load(f)
            discrepancy_list.extend(entries_for_discrepancies)

        with open(discrepancies_file, "w") as f:
            json.dump(discrepancy_list, f, ensure_ascii=False, indent=4)
        # print(f"{len(entries_for_discrepancies)} discrepancies saved to file")

# create a logging file to check data processing numbers
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    total_records = len(records)

    log_entry = {
        "timestamp": timestamp,
        "topic": topic,
        "kp_entries": len(base_entries),
        "p_entries": len(match_entries),
        "records_created": total_records,
        "matches_found": len(p_entries_matched),
        "discrepancies": len(entries_for_discrepancies)
        }

    if not processing_log.exists():
        raise FileNotFoundError("process_log file missing!")
    else:
        with open(processing_log, "r") as f:
            process_report = json.load(f)
            process_report.append(log_entry)

        with open(processing_log, "w") as f:
            json.dump(process_report, f, ensure_ascii=False, indent=4)

    # handle erstausgaben

    if topic_normalised in ["erstausgaben1", "erstausgaben2"]:
        return
    elif topic_normalised == "erstausgaben3":
        # load json files, combine them into unified records, move on to batching
        path1 = path / "erstausgaben1.json"
        path2 = path / "erstausgaben2.json"
        with open(path1, "r") as f1:
            erstausgaben1 = json.load(f1)
        with open(path2, "r") as f2:
            erstausgaben2 = json.load(f2)
        ea_combined = erstausgaben1 + erstausgaben2 + records
        records = ea_combined
        total_records = len(records)
        pass


# BATCHING SECTION

# records: a LIST of DICTIONARIES, each record is a dictionary, and all of them are stored in a list

# 1. Create folder structure
    folder = Path("data/batched")
    batch_folder = folder / topic_normalised
    batch_folder.mkdir(exist_ok=True)


# 2. Calculate batch information
    batch_size = 25
    total_batches = (total_records + batch_size - 1) // batch_size

# 3. Add batch information to each record
    for index, record in enumerate(records):
        if record["topic_normalised"] in ["erstausgaben1", "erstausgaben2", "erstausgaben3"]:
            record["topic_normalised"] = "erstausgaben"

        batch_id = (index // batch_size) + 1
        record["record_index"] = index
        record["batch_id"] = batch_id
        record["total_batches"] = total_batches
        record["composite_id"] = f"{topic_normalised}_{index}_{batch_id}_{total_batches}"

    # pp(records)

# 4. Group records into batches and save as JSON files
    batches = {}
    for record in records:
        batch_id = record["batch_id"]
        if batch_id not in batches:
            batches[batch_id] = []
        batches[batch_id].append(record)

    for batch_id, batch_records in batches.items():
        filename = f"{topic_normalised}_{batch_id}-{total_batches}.json"

        path = batch_folder / filename

        with open(path, "w") as f:
            json.dump(batch_records, f, ensure_ascii=False, indent=4)
            pp(f"{filename} successfully saved")

# consolidate_entries("ISLAM.docx")
    pass
    # pp(len(batches[4]))
