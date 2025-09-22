import json
from datetime import datetime
import time
from pathlib import Path
from pprint import pp
from load_entries import prepare_entries, load_entries

# New approach
# Orchestrator → Prep → Status back to Orchestrator → Load → Status back to Orchestrator

log_file = Path("data/logs/data_loading_log.json")
folder_path = Path("data/parsed")
# hardcoded for now! TODO get from parsed files
# filename = Path("data/parsed/batch_aegypten_20250911-2255.json")

def get_parsed_files():
    parsed_dir = Path("data/parsed")
    parsed_files = []

    if not parsed_dir.exists():
        raise NotADirectoryError("Directory doesn't exist!")

    for file in parsed_dir.glob("*.json"):
        parsed_files.append(file.name)

    return parsed_files

def read_log():
    if not log_file.exists():
        raise FileNotFoundError("Log file missing!")
    else:
        with open(log_file, "r") as f:
            db_loading_log = json.load(f)

    return db_loading_log
# read_log()

def get_files_for_processing():
    available_files = get_parsed_files()
    db_loading_log = read_log()
    processed_files = []

    for processed_file in db_loading_log:
        filename = processed_file["filename"]
        processing_done = processed_file["processing_done"]

        if processing_done:
            processed_files.append(filename)

    files_to_process = [file for file in available_files if str(file) not in processed_files]

    # filename = files_to_process[0]

    return files_to_process


def prep_and_load_files():
    start_time = time.time()
# 1. get list
    files_for_processing = get_files_for_processing()
    file_count = 0
# 2. loop through list, log each part of the process separately
    for filename in files_for_processing:
        prep_status = prepare_entries(filename)
        current_log = read_log()
        log_entry = {
            "filename": prep_status["filename"],
            "processing_done": prep_status["processing_done"],
            "loading_done": prep_status["loading_done"],
            "entry_count": prep_status["entry_count"],
            "people_logged": prep_status["people_logged"],
            "timestamp": prep_status["timestamp"]
        }
        current_log.append(log_entry)

        with open(log_file, "w") as f:
            json.dump(current_log, f, ensure_ascii=False, indent=2)

        if prep_status["processing_done"]:
            load_status = load_entries(prep_status)

            for entry in current_log:
                if entry["filename"] == prep_status["filename"]:
                    entry["loading_done"] = load_status["loading_done"]
                    entry["timestamp_loading"] = load_status["timestamp_loading"]
                    break

            with open(log_file, "w") as f:
                json.dump(current_log, f, ensure_ascii=False, indent=2)

        if prep_status["processing_done"] and load_status["loading_done"]:
            file_count += 1
    end_time = time.time()
    duration = end_time - start_time
    pp(f"{file_count} entries were prepped & loaded successfully in {duration:.2f} seconds 🥳")

def main():
    prep_and_load_files()

if __name__ == "__main__":
    main()

# 3. print an overview of the results to the console (the logging data is saved anyway, I don't need to store that as well)


# get_parsed_files()
