from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
sys.path.append(str(Path(__file__).parent.parent))

from scripts.text_matching import normalise_text

folder_parsedfolder_prepped = Path("data/prepped")
people_file = Path("data/people/people_extracted.json")
variants_file = Path("data/from db/people_variants.json")


matched_file = Path("data/people/people_matched.json")
unmatched_file = Path("data/people/people_unmatched.json")

def match_people2variants():
    with open(people_file, "r") as f:
        people_dict = json.load(f)

    with open(variants_file, "r") as f:
        variants = json.load(f)

    variants_dict = {normalise_text(variant["variant_normalised"]): variant for variant in variants}

    matched = {}
    unmatched = {}

    matched_count = 0
    unmatched_count = 0

    for name, values in people_dict.items():
        if name in variants_dict:
            variant = variants_dict[name]
            matched[name] = {
                "variant_id": variant["variant_id"],
                "person_id": variant["person_id"],
                "unified_id": variant["unified_id"],
                "occurrences": values
            }
            matched_count += 1
        else:
            unmatched[name] = values
            unmatched_count += 1

    unique_people = len(people_dict)
    percent_matched = (matched_count / unique_people) * 100
    percent_unmatched = (unmatched_count / unique_people) * 100


    matching_log = {
        "unique_people": unique_people,
        "people_occurrences": sum(len(v) for v in people_dict.values()),
        "matched": matched_count,
        "pct_matched": percent_matched,
        "unmatched": unmatched_count,
        "pct_unmatched": percent_unmatched
        }

    rprint(matching_log)

    with open(matched_file, "w") as f:
        json.dump(matched, f, ensure_ascii=False, indent=2)
    with open(unmatched_file, "w") as f:
        json.dump(unmatched, f, ensure_ascii=False, indent=2)

match_people2variants()
