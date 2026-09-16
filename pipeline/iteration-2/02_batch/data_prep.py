from datetime import datetime
import os
from pathlib import Path
import re
import json
from rich import print, inspect
import unicodedata

processing_log = Path("data/logs/processing_log.json")
prepped_folder = Path("data/raw/prepped")
folder = Path("data/batched")

def create_batches():
    records = []

    for file in prepped_folder.iterdir():
        topic_normalised = file.stem

        with open(file, "r") as f:
            records = json.load(f)

        total_records = len(records)

        if topic_normalised in ["erstausgaben1", "erstausgaben2"]:
            continue
        elif topic_normalised == "erstausgaben3":
            # load json files, combine them into unified records, move on to batching
            path1 = prepped_folder / "erstausgaben1.json"
            path2 = prepped_folder / "erstausgaben2.json"
            with open(path1, "r") as f1:
                erstausgaben1 = json.load(f1)
            with open(path2, "r") as f2:
                erstausgaben2 = json.load(f2)
            ea_combined = erstausgaben1 + erstausgaben2 + records
            records = ea_combined
            topic_normalised = "erstausgaben"
            total_records = len(records)
            pass


    # 1. Create folder structure
        folder = Path("data/raw/batched")
        batch_folder = folder / topic_normalised
        batch_folder.mkdir(parents=True, exist_ok=True)


# 2. Calculate batch information
        batch_size = 25
        total_batches = (total_records + batch_size - 1) // batch_size

# 3. Add batch information to each record
        for index, record in enumerate(records):

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
                print(f"{filename} successfully saved")

create_batches()
