import json
from datetime import datetime
from pathlib import Path
from pprint import pp
from load_entries import prepare_entries

# New approach
# Orchestrator → Prep → Status back to Orchestrator → Load → Status back to Orchestrator

log_file = Path("data/logs/data_loading_log.json")

# hardcoded for now! TODO get from parsed files
filename = Path("data/parsed/batch_aegypten_20250911-2255.json")

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
            # pp(type(db_loading_log))
            # pp(db_loading_log)
    return db_loading_log
# read_log()

def get_file_for_processing():
    available_files = get_parsed_files()
    db_loading_log = read_log()
    processed_files = []

    for processed_file in db_loading_log:
        filename = processed_file["filename"]
        processing_done = processed_file["processing_done"]

        if processing_done:
            processed_files.append(filename)
    pp(processed_files)

    files_to_process = [f for f in available_files if str(f) not in processed_files]
    pp(files_to_process)
    filename = files_to_process[0]
    pp(filename)

    return filename
files = get_file_for_processing()

def log_data_processing(db_loading_log=None):
    status = prepare_entries(filename)

    log_entry = [{
        "filename": status["filename"],
        "processing_done": status["processing_done"],
        "loading_done": status["loading_done"],
        "entry_count": status["entry_count"],
        "people_logged": status["people_logged"],
        "timestamp": status["timestamp"]
    }]

    db_loading_log.append(log_entry)

    with open(log_file, "w") as f:
        json.dump(db_loading_log, f, ensure_ascii=False, indent=2)
    return db_loading_log

#  log_data = log_data_processing()






# get_parsed_files()
