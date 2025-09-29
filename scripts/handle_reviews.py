import json
import re
import ijson
from pathlib import Path
from pprint import pp

review_log = Path("data/logs/review_entries_log.json")
to_review_file = Path("database/to_review.json")

def get_entries_for_review():
    to_check = []
    references = []
    review_content = {
        "high": {},
        "medium": {}
    }

    with open(review_log, "r") as f:
        i = 0
        for entry in ijson.items(f, "item"):
            review_done = False
            i += 1

            original_text = str(entry["parsed_entry"]["administrative"]["original_entry"])
            notes = str(entry["parsed_entry"]["administrative"].setdefault("verification_notes", ""))
            confidence = entry["parsed_entry"]["administrative"]["parsing_confidence"]
            siehe = re.search("[sS]iehe", original_text)
            reference = re.search("reference", notes)

            if siehe or reference:
                if confidence == "low":
                    references.append(entry)

            if confidence != "low":
                to_check.append(entry)

        for entry in to_check:
            if confidence == "high":
                review_content["high"].append({
                    "original": original_text,
                    "notes": notes,

                })



    pp(f"references {len(references)}")
    pp(f"to_check {len(to_check)}")
    pp(f"total: {i}")


get_entries_for_review()
