from docx import Document
import csv
import os
import re
from pprint import pp


folder_preise = "data/original/preise/"
folder_keinepreise = "data/original/keine preise/"
files_info = "data/files_info_header.csv"
discrepancies_file = "data/discrepancies.json"

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

        topic = filename.replace(".docx", "")
        topic_normalised = topic.lower().split()[0]
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

                    text_normalised = price_removed.replace('\n', '. ')
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

    records = {}
    discrepancies = {}
    p_entries_matched = set()

# 2. Loop through base_entries using enumerate to get both index and entry
# 3. For each base_entry, first try to match at the same index in match_entries

    for index, base_entry in enumerate(base_entries):
        # pp({"index": index, "entry": base_entry})
        if index < len(match_entries):
            if base_entry["text"].strip() == match_entries[index]["text"].strip():
                p_entries_matched.add(index)
                # pp(f"found a match at {index}")
            else:
                for search_index, match_entry in enumerate(match_entries):
                    if base_entry["text"].strip() == match_entry["text"].strip():
                        match_found_at_index = None
                        match_found_at_index = search_index
                        p_entries_matched.add(search_index)
                        # pp(f"found a match for {index} at {match_found_at_index}.")
                        break

    p_indices = set(range(len(match_entries)))
    unmatched_indices = p_indices - p_entries_matched
    pp(unmatched_indices)


#
#    - Check if index exists in match_entries (index < len(match_entries))
#    - If it exists, compare base_entry["text"] with match_entries[index]["text"]
#    - Use string comparison that ignores extra whitespace (.strip() and normalize spaces)
#   if base_entry["text"].strip() == match_entry["text"].strip():
#   -> add current index to matched_p_indices

# 4. If same-index match fails, search through all of match_entries
#    - Loop through entire match_entries list
#    - Compare base_entry["text"] with each match_entry["text"]
#    - If match found, remember which index it was found at
#
#       match_found_at_index = None  # Initialize as None (meaning no match found yet)
#
#       for search_index, match_entry in enumerate(match_entries):
#           if base_entry["text"].strip() == match_entry["text"].strip():
#               match_found_at_index = search_index  # Remember where we found it
#               add index to matched_p_indices
#               break  # Stop searching once we find it


# 5. Handle matches

#       if match_found_at_same_index:
#           # Handle match - use kp text + p price
#       elif match_found_at_different_index:
#           # Handle match - use kp text + p price
#       else:
#           # No match found - use kp text + no price

# 6. Create matched record when match is found
#    - Use "text" from the 'kp' version (always authoritative)
#    - Use price from 'p' version if it exists, otherwise None
#    - Use "topic" and "topic_normalized" from 'kp' version (always authoritative)
#    - Remove "source" field as it's no longer needed
#       # Create and append the new record in one step
        # records.append({
        #     "text": kp_text,
        #     "price": p_price,
        #     "topic": kp_topic,
        #     "topic_normalized": kp_topic_normalized
        # })

# 7. Add unmatched entries to discrepancies
#    - Use the indices that are NOT in matched_p_indices
#    - Only unmatched 'p' entries (entries that exist in p but not in kp)
#    - Include the full 'p' entry for review
#    - These represent entries that were removed from the authoritative kp version

#   After all kp entries are processed, find unmatched p entries
#   indices = set()

# 8. Write discrepancies into file
#    1. check if file exists
#       - NO: throw error, stop
#       - YES: continue
#    2. use json.load() to read current file
#    3. append entries from discrepancies list
#    4. save the new list to file
#    5. close file


# BATCHING SECTION

# 1. Topic normalization fixes
#    - Check if topic contains "ERSTAUSGABEN" - if yes, set both topic and topic_normalized to "erstausgaben"
#    - Check if topic is "DEUTSCHE LITERATUR MONOGRAPHIEN" - if yes, set topic_normalized to "deutsche-literatur-monographien"
#    - Check if topic is "DEUTSCHE LITERATUR TEXTE" - if yes, set topic_normalized to "deutsche-literatur-texte"

# Process each file individually (discrepancies handled internally)
    # records_A = consolidate_entries("ERSTAUSGABEN A - G")
    # records_B = consolidate_entries("ERSTAUSGABEN H - M")
    # records_C = consolidate_entries("ERSTAUSGABEN N - Z")

    # # 2. COMBINATION STEP
    # if topic_normalized == "erstausgaben":
    #     combined_records = records_A + records_B + records_C
    # else:
    #     combined_records = records

# 2. Create folder structure
#    - Create path: data/batched/{topic_normalized}/
#    - Use os.makedirs() with exist_ok=True
#    - Check if folder exists after creation, if not, raise error and stop

# 3. Calculate batch information
#    - Get total number of records: len(records)
#    - Calculate number of batches: math.ceil(total_records / 25)
#    - Store batch_size = 25 as variable

# 4. Add batch information to each record
#    - Loop through records with enumerate to get index
#    - Calculate batch_id: (index // batch_size) + 1
#    - Add batch_id to each record
#    - Add batch_total to each record
#    - Add entry_index to each record (this is the enumerate index)
#    - Create composite_id: f"{topic_normalized}_{entry_index}_{batch_id}_{batch_total}"
#    - Add composite_id to each record

# 5. Group records into batches and save as JSON files
#    - Loop through batch numbers (1 to batch_total)
#    - For each batch, collect all records where batch_id matches current batch number
#    - Create filename: f"{topic_normalized}_batch_{batch_id}_of_{batch_total}.json"
#    - Create full filepath: data/batched/{topic_normalized}/{filename}
#    - Write batch records to JSON file using json.dump()
#    - Check if file was created successfully, if not, raise error

# 6. Print success message
#    - Print total number of records processed
#    - Print number of batches created
#    - Print number of discrepancies found
#    - Confirm all files created successfully

# 7. Return values
#    - Return records dictionary and discrepancies dictionary for further processing



    # pp(f"For {topic}: base has {len(base_entries)} entries, match has {len(match_entries)} entries")
    # pp(f"For {topic}: using {'p' if base_entries == entries['p'] else 'kp'} as base ({len(base_entries)} entries), matching against {len(match_entries)} entries")

    # pp(entries["p"][5], width=150)
    # pp(entries["p"][12])
    # pp(entries["kp"][12])
    # pp(entries["kp"][17], width=150)
    # pp(entries["p"])


consolidate_entries("ÄGYPTEN VORDERER ORIENT.docx")

# get_entries("ZEITSCHRIFTEN.docx", folder_preise)
