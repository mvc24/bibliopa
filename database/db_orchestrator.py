import json
from datetime import datetime
from pathlib import Path
from pprint import pp

def get_parsed_files():
    parsed_dir = Path("data/parsed")
    parsed_files = []

    if not parsed_dir.exists():
        raise NotADirectoryError("Directory doesn't exist!")

    for file in parsed_dir.glob("*.json"):
        parsed_files.append(file.name)

#    pp(parsed_files)

    return parsed_files

get_parsed_files()

#
# New approach
# Orchestrator → Prep → Status back to Orchestrator → Load → Status back to Orchestrator

# check which files are available for reading into the database
# compare available filenames with the log file for previously processed files (flag is_processed: True)
# get filename of next file to process where is_processed == False
# send filename to `database/load_entries.py` file which will contain all the necessary functions to transform the json file into database tables (I have the mapping and schema and everything built)
# return the filename and is_processed: True to db_orchestrator.py

# def create_log():
#     db_log_entry = {}

#     log_file = Path("data/logs/data_loading_log.json")
#     if not log_file.exists():
#         raise FileNotFoundError("Log file missing!")
#     else:
#         with open(log_file, "r") as f:
#             db_loading_log = json.load(f)
#             db_loading_log.append(db_log_entry)

#         with open(log_file, "w") as f:
#             json.dump(db_loading_log, f, ensure_ascii=False, indent=2)
