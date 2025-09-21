import json
from datetime import datetime
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

#    pp(parsed_files)

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

# files = get_file_for_processing()

# run data prep with found file

# prepare_entries(filename)

# def log_data_prep(db_loading_log=None):
#     prep_status = prepare_entries(filename)

#     log_entry = [{
#         "filename": prep_status["filename"],
#         "processing_done": prep_status["processing_done"],
#         "loading_done": prep_status["loading_done"],
#         "entry_count": prep_status["entry_count"],
#         "people_logged": prep_status["people_logged"],
#         "timestamp": prep_status["timestamp"]
#     }]

#     db_loading_log.append(log_entry)

#     with open(log_file, "w") as f:
#         json.dump(db_loading_log, f, ensure_ascii=False, indent=2)
#     return db_loading_log

def prep_and_load_files():

# 1. get list
    files_for_processing = get_files_for_processing()

# 2. loop through list
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

# 2a. for each file in the list: prepare_entries(filename), return status

# 2b. move logging function in here for prep log



        # log_entry = [{
        #     "filename": prep_status["filename"],
        #     "processing_done": prep_status["processing_done"],
        #     "loading_done": prep_status["loading_done"],
        #     "entry_count": prep_status["entry_count"],
        #     "people_logged": prep_status["people_logged"],
        #     "timestamp": prep_status["timestamp"]
        # }]

        # db_loading_log.append(log_entry)

# 2c. call load_entries(prepared_entries), return loading_status

# 2d. append loading status to log

# 2e. add a counter to print a success/failure message at the end?

# 3. print an overview of the results to the console (the logging data is saved anyway, I don't need to store that as well)


# NOT SURE HOW TO HANDLE THIS:
# Option 1: once both processing_done & loading_done are TRUE, remove the current filename from the list (or is that not necessary?). Only update json file at the end of the loop.
    # Pro: One list is worked through sequentially, less json opening/closing/rewriting, the log is created for one entire file processing loop, however many unprocessed files there were found at the beginning of the process. If new files are parsed & saved WHILE this process is running, it doesn't interfere with the list but the orchestrator can be started freshly afterwards.

# Option 2: create the processing list WITHIN the loop for each file?
    # Pro: would instantly add new files if parser & loading process run parallel.
    # Con: it feels harder to "supervise", could lead to issues? Doesn't feel as safe?

# 2e. write log for 1 file to json

        # with open(log_file, "w") as f:
        #     json.dump(db_loading_log, f, ensure_ascii=False, indent=2)
        # return db_loading_log









# get_parsed_files()
