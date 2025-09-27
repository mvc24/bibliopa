import ijson
import re
from pathlib import Path
from pprint import pp
import json

ex_corrupt_log = Path("data/logs/corrupt_entries_log.json")
ex_corrupt = Path("data/logs/ex_corrupt.json")
yay_clean_file = Path("data/logs/yay_clean.json")
really_clean_file = Path("data/parsed/really_clean_now.json")

def get_data():
    entries_new = []

    with open(ex_corrupt_log, "r") as f:
        entries = json.load(f)
        # for entry in ijson.items(f, "item"):
        for entry in entries:
            # pp(f"entry: {type(entry)}")
            # pp(f"entries: {type(entries)}")
            raw_entry = entry["raw_response"]
            entries_new.append({
                "custom_id": entry["custom_id"],
                "parsed_entry": raw_entry
            })

    with open(ex_corrupt, "w") as f:
        json.dump(entries_new, f, ensure_ascii=False, indent=2)

    pp(f"raw entry outside loop: {raw_entry}")

# get_data()

def cleanup():
    yay_clean_data = []
    with open(ex_corrupt, "r") as f:
        data = json.load(f)

    for entry in data:
        str2clean = entry["parsed_entry"]
        n = r"\n\s*"
        # lq =
        rq = r'\\"'
        s = re.sub(n, "", str2clean)
        clean = re.sub(rq, chr(8220), s)
        yay_clean_data.append({
            "custom_id": entry["custom_id"],
            "parsed_entry": clean
        })

    with open(yay_clean_file, "w") as f:
        json.dump(yay_clean_data, f, ensure_ascii=False, indent=2)

        # pp(clean)

    #low: chr(8222)
    #high: chr(8220)
cleanup()

def check_json():
    correct_data = []
    errors = []

    with open(yay_clean_file, "r") as f:
        content = json.load(f)

    for entry in content:
        try:
            dict_data = json.loads(entry["parsed_entry"])
            correct_data.append({
                "custom_id": entry["custom_id"],
                "parsed_entry": dict_data
            })
        except json.JSONDecodeError as e:
            errors.append({
                "custom_id": entry["custom_id"],
                "error": str(e)
            })
    with open(really_clean_file, "w") as f:
        json.dump(correct_data, f, ensure_ascii=False, indent=2)

    pp(f"I did it!")
    if errors:
        pp(f"nope. {len(errors)} found. Alas.")
check_json()
