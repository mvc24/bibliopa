import json
import re
from pathlib import Path

# File paths
people_file = Path("database/in_progress/collect_people.json")
batch_output_dir = Path("database/in_progress/pass1_batches")
log_file = Path("database/in_progress/pass1_preparation.log")

def identify_multi_person_entries(entries):
    """
    Filter entries that contain multiple people.

    Returns:
        list: Entries that need to be split
    """
    multi_person_entries = []

    # Patterns indicating multiple people
    und_pattern = re.compile(r' und ', re.IGNORECASE)
    u_dot_pattern = re.compile(r' u\. ', re.IGNORECASE)

    for entry in entries:
        display_name = entry.get("display_name") or ""
        single_name = entry.get("single_name") or ""
        family_name = entry.get("family_name")
        given_names = entry.get("given_names")

        # Check if family_name and given_names are both null/None
        is_unparsed = (family_name is None or family_name == "null") and \
                      (given_names is None or given_names == "null")

        # Check for multi-person patterns in display_name or single_name
        has_und = und_pattern.search(display_name) or und_pattern.search(single_name)
        has_u_dot = u_dot_pattern.search(display_name) or u_dot_pattern.search(single_name)

        # If unparsed AND has multi-person indicators, it needs splitting
        if is_unparsed and (has_und or has_u_dot):
            multi_person_entries.append(entry)

    return multi_person_entries


def create_batches(entries, batch_size=25):
    """
    Split entries into batches of specified size.

    Returns:
        list: List of batches, each batch is a list of entries
    """
    batches = []

    for i in range(0, len(entries), batch_size):
        batch = entries[i:i+batch_size]
        batches.append(batch)

    return batches


def main():
    # Load all people entries
    print(f"Loading people data from {people_file}...")
    with open(people_file, "r", encoding="utf-8") as f:
        all_entries = json.load(f)

    print(f"Total entries loaded: {len(all_entries)}")

    # Identify entries that need splitting
    multi_person_entries = identify_multi_person_entries(all_entries)

    print(f"Entries needing split: {len(multi_person_entries)}")

    if len(multi_person_entries) == 0:
        print("No entries found that need splitting. Exiting.")
        return

    # Create batches
    batches = create_batches(multi_person_entries, batch_size=25)

    print(f"Created {len(batches)} batches")

    # Create output directory if it doesn't exist
    batch_output_dir.mkdir(parents=True, exist_ok=True)

    # Save batches
    for idx, batch in enumerate(batches, start=1):
        batch_file = batch_output_dir / f"batch_split_{idx:02d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"Saved {batch_file} ({len(batch)} entries)")

    # Create summary log
    summary = {
        "total_entries_scanned": len(all_entries),
        "entries_needing_split": len(multi_person_entries),
        "batches_created": len(batches),
        "batch_size": 25,
        "output_directory": str(batch_output_dir)
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nSummary log saved to {log_file}")
    print(f"Batches ready for Pass 1 API processing!")


if __name__ == "__main__":
    main()
