import json
import re
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).parent.parent

nopes_file = project_root / "scripts/notebooks/nopes_fixed.json"
people_file = project_root / "data/from db/people.json"
batch_output_dir = project_root / "database/in_progress/nopes_batches"
log_file = project_root / "database/in_progress/nopes_prep.log"

BATCH_SIZE = 30


def normalize_surname(name):
    if not name:
        return "unknown"
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()


def build_existing_lookup(people):
    lookup = defaultdict(list)
    for person in people:
        family_name = person.get("family_name") or person.get("single_name") or ""
        key = normalize_surname(family_name)
        lookup[key].append({
            "person_id": person["person_id"],
            "unified_id": person["unified_id"],
            "family_name": person.get("family_name"),
            "given_names": person.get("given_names"),
            "name_particles": person.get("name_particles"),
            "single_name": person.get("single_name"),
            "is_organisation": person.get("is_organisation", False)
        })
    return lookup


def main():
    print(f"Loading nopes from {nopes_file}...")
    with open(nopes_file, "r", encoding="utf-8") as f:
        nopes = json.load(f)

    print(f"Loading existing people from {people_file}...")
    with open(people_file, "r", encoding="utf-8") as f:
        people = json.load(f)

    print(f"Nopes: {len(nopes)}, Existing people: {len(people)}")

    existing_lookup = build_existing_lookup(people)
    print(f"Built existing people lookup with {len(existing_lookup)} surname groups")

    # Convert nopes dict to list, embedding display_norm as a field
    nopes_list = []
    for display_norm, entry in nopes.items():
        nopes_list.append({
            "display_norm": display_norm,
            "composite_id": entry["composite_id"],
            "family_name": entry.get("family_name"),
            "given_names": entry.get("given_names"),
            "name_particles": entry.get("name_particles"),
            "single_name": entry.get("single_name"),
            "last_norm": entry.get("last_norm"),
            "first_norm": entry.get("first_norm"),
            "single_norm": entry.get("single_norm"),
            "is_organisation": entry.get("is_organisation", False)
        })

    # Group by last_norm so similar surnames go into the same batch
    groups = defaultdict(list)
    for entry in nopes_list:
        key = entry.get("last_norm") or normalize_surname(entry.get("single_norm") or "")
        groups[key].append(entry)

    print(f"Surname groups in nopes: {len(groups)}")

    # Create batches, keeping surname groups together
    batches = []
    current_nopes = []
    current_keys = set()

    for surname_key, entries in sorted(groups.items()):
        if len(current_nopes) + len(entries) > BATCH_SIZE and current_nopes:
            batches.append((current_nopes, list(current_keys)))
            current_nopes = []
            current_keys = set()
        current_nopes.extend(entries)
        current_keys.add(surname_key)

    if current_nopes:
        batches.append((current_nopes, list(current_keys)))

    print(f"Created {len(batches)} batches")

    batch_output_dir.mkdir(parents=True, exist_ok=True)

    for idx, (nopes_entries, context_keys) in enumerate(batches, start=1):
        context_people = []
        for key in context_keys:
            context_people.extend(existing_lookup.get(key, []))

        batch_data = {
            "nopes_entries": nopes_entries,
            "existing_people_context": context_people
        }

        batch_file = batch_output_dir / f"batch_nopes_{idx:03d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        print(f"  Saved {batch_file.name} ({len(nopes_entries)} nopes, {len(context_people)} context)")

    summary = {
        "total_nopes": len(nopes_list),
        "total_existing": len(people),
        "batches_created": len(batches),
        "output_directory": str(batch_output_dir)
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nSummary saved to {log_file}")
    print(f"Batches ready for Operation B (nopes dedup + clean)!")
    print(f"  Total nopes entries: {len(nopes_list)}")
    print(f"  Total batches: {len(batches)}")


if __name__ == "__main__":
    main()
