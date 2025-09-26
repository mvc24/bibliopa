import json
from datetime import datetime
import time
from pathlib import Path
from pprint import pp
from load_entries import prepare_entries, load_entries


log_file = Path("data/logs/data_loading_log.json")
folder_path = Path("data/parsed")

def get_parsed_files():
    parsed_dir = Path("data/parsed")
    parsed_files = set()

    if not parsed_dir.exists():
        raise NotADirectoryError("Directory doesn't exist!")

    for file in parsed_dir.glob("*.json"):
        parsed_files.add(file.name)

    return parsed_files


def read_log():
    if not log_file.exists():
        raise FileNotFoundError("Log file missing!")
    try:
        with open(log_file, "r") as f:
            db_loading_log = json.load(f)
        return db_loading_log

    except json.JSONDecodeError:
        db_loading_log = {
            "entries": [],
            "completed": [],
            "failed": []
        }
        return db_loading_log
# read_log()

def get_files_for_processing():
    available_files = get_parsed_files()
    db_loading_log = read_log()
    processed_files = set(db_loading_log.setdefault("completed", []))
    error_files = set(db_loading_log.setdefault("failed", []))

    files_to_process = available_files - processed_files - error_files

    return files_to_process

def prep_and_load_files():
    start_time = time.time()

# 1. get list
    files_for_processing = get_files_for_processing()
    # pp(f"")
    file_count = 0
    total_entries_loaded = 0
    total_corrupt_entries = 0
# 2. loop through list, log each part of the process separately
    for filename in files_for_processing:
        prep_status = prepare_entries(filename)
        current_log = read_log()

        current_log.setdefault("entries", []).append({
            "filename": prep_status["filename"],
            "success": prep_status["success"],
            "critical_error": prep_status["critical_error"],
            "error_message": prep_status["error_message"],
            "processing_done": prep_status["processing_done"],
            "loading_done": prep_status["loading_done"],
            "entry_count": prep_status["entry_count"],
            "people_logged": prep_status["people_logged"],
            "corrupt_entries_found": prep_status["corrupt_entries_found"],
            "timestamp": prep_status["timestamp"]
        })

        if prep_status["critical_error"] or not prep_status["processing_done"]:
            current_log.setdefault("failed", []).append(prep_status["filename"])

        with open(log_file, "w") as f:
            json.dump(current_log, f, ensure_ascii=False, indent=2)

        if prep_status["processing_done"]:
            load_status = load_entries(prep_status)

            for entry in current_log.setdefault("entries", []):
                if entry["filename"] == prep_status["filename"]:
                    entry["critical_error_loading"] = load_status["critical_error_loading"]
                    entry["error_message_loading"] = load_status["error_message_loading"]
                    entry["loading_done"] = load_status["loading_done"]
                    entry["timestamp_loading"] = load_status["timestamp_loading"]
                    break

            if load_status["critical_error_loading"] or not load_status["loading_done"]:
                current_log.setdefault("failed", []).append(load_status["filename"])

            if prep_status["processing_done"] and load_status["loading_done"]:
                file_count += 1
                total_entries_loaded += prep_status["entry_count"]
                total_corrupt_entries += prep_status["corrupt_entries_found"]
                current_log.setdefault("completed", []).append(load_status["filename"])

            with open(log_file, "w") as f:
                json.dump(current_log, f, ensure_ascii=False, indent=2)

    end_time = time.time()
    duration = end_time - start_time

    # Create comprehensive success message
    if total_corrupt_entries > 0:
        pp(f"{file_count} files processed, {total_entries_loaded} entries loaded, {total_corrupt_entries} corrupt entries quarantined in {duration:.2f} seconds 🥳")
    else:
        pp(f"{file_count} files processed, {total_entries_loaded} entries loaded successfully in {duration:.2f} seconds 🥳")

def main():
    prep_and_load_files()

if __name__ == "__main__":
    main()

# 3. print an overview of the results to the console (the logging data is saved anyway, I don't need to store that as well)


# get_parsed_files()
