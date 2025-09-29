import time
import json
from datetime import datetime
from pathlib import Path
from text_matching import test_similarity, normalise_text
from progress import progress
from pprint import pp

consolidated_dir = Path("data/consolidated")
processed_discrepancies_file = Path("data/logs/discrepancies_processed.json")
original_discrepancies_file = Path("data/discrepancies.json")
collected_entries_file = Path("database/in_progress/collected_entries.json")

def resolve_discrepancies():

    filenames = set()
    collected_entries = []
    processed_discrepancies = {}
    resolved = processed_discrepancies.setdefault("resolved", [])
    resolved_ish = processed_discrepancies.setdefault("resolved_ish", [])
    unresolved = processed_discrepancies.setdefault("unresolved", [])

    if not consolidated_dir.exists():
        raise NotADirectoryError("consolidated_dir doesn'T exist!")
    if not original_discrepancies_file.exists():
        raise FileNotFoundError("Discrepancies file missing!")
    if not processed_discrepancies_file.exists():
        raise FileNotFoundError("processed_discrepancies file missing!")
    if not collected_entries_file.exists():
        raise FileNotFoundError("collected_entries_file doesn't exist")

# 1. collect all entries

    try:
        for file in consolidated_dir.glob("*.json"):
            filenames.add(file.name)

        for file in filenames:
            full_path = Path(consolidated_dir / file)

            with open(full_path, "r") as f:
                entries = json.load(f)
                collected_entries.extend(entries)

        with open(collected_entries_file, "w") as f:
            json.dump(collected_entries, f, ensure_ascii=False, indent=2)

    except json.JSONDecodeError as e:
        pp(f"Something went wrong: {e}")

# 2. get discrepancies
    with open(original_discrepancies_file, "r") as f:
        discrepancies = json.load(f)


# 3. build lookup dict and start searching
    collected_lookup = {normalise_text(entry["text"]): entry for entry in collected_entries}
    sort_collected = sorted(collected_lookup.items())

    total_discrepancies = len(discrepancies)

    start = time.perf_counter()
    start_stamp = datetime.now().strftime("%H:%M:%S")
    print(f"Started at: {start_stamp}")

    for i, discrepancy in enumerate(discrepancies):
        progress(i + 1, total_discrepancies)

        discrepancy_norm = normalise_text(discrepancy["text"])
        if discrepancy_norm in collected_lookup:
            matched_entry = collected_lookup[discrepancy_norm]
            resolved.append({
                **discrepancy,
                "matched_topic": matched_entry["topic"],
                "matched_price": matched_entry["price"]
            })
        else:
            best_score = 0
            best_entry = None
            best_match = None
            for collected_text, collected_entry in sort_collected:
                score = test_similarity(discrepancy_norm, collected_text)
                if score > best_score:
                    best_score = score
                    best_entry = collected_entry
                    best_match = collected_text

                if score >= 95:
                    resolved.append({
                        **discrepancy,
                        "matched_topic": collected_entry["topic"],
                        "matched_price": collected_entry["price"],
                        "score": score,
                        "original_text": discrepancy["text"],
                        "matched_text": collected_entry["text"]
                    })
                    break

            if best_score < 95 and best_score >= 75:
                resolved_ish.append({
                    **discrepancy,
                    "highest_score": best_score,
                    "best_match": best_match,
                    "best_match_topic": best_entry["topic"]
                })
            elif best_score < 75:
                unresolved.append({
                    **discrepancy,
                    "highest_score": best_score,
                    "best_match": best_match,
                    "best_match_topic": best_entry["topic"]
                })


# 4. save to file

    with open(processed_discrepancies_file, "w") as f:
        json.dump(processed_discrepancies, f, ensure_ascii=False, indent=2)

    done = time.perf_counter()
    done_stamp = datetime.now().strftime("%H:%M:%S")
    duration = done - start

    print(f"  ")
    print(f"Done at: {done_stamp}")
    print(f"resolved: {len(resolved)} discrepancies.")
    print(f"Probably resolved {len(resolved_ish)} entries.")
    print(f"{len(unresolved)} remain unresolved.")
    print(f"This took {duration:.2f} seconds. That's {duration / 60:.2f} minutes")
resolve_discrepancies()
