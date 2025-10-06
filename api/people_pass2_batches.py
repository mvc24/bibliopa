import json
import re
from pathlib import Path
from collections import defaultdict

# File paths
people_file = Path("database/in_progress/collect_people.json")
pass1_results_dir = Path("database/in_progress/pass1_results")
batch_output_dir = Path("database/in_progress/pass2_batches")
log_file = Path("database/in_progress/pass2_preparation.log")


def normalize_for_grouping(name):
    """
    Normalize a name for grouping similar names together.
    This is just for batching efficiency, not for final deduplication.
    """
    if not name:
        return "unknown"

    # Convert to lowercase and remove special characters
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def group_people_by_surname(entries):
    """
    Group people entries by normalized surname for efficient batching.
    Returns dict: {normalized_surname: [entries]}
    """
    groups = defaultdict(list)

    for entry in entries:
        # Try to get family_name, fallback to extracting from display_name
        family_name = entry.get("family_name")

        if not family_name or family_name == "null":
            # Try to extract from display_name
            display_name = entry.get("display_name") or ""
            # Common German format is "SURNAME, Given" or "Surname, Given"
            if display_name and "," in display_name:
                family_name = display_name.split(",")[0].strip()
            else:
                # Fallback: use last word
                words = display_name.split()
                family_name = words[-1] if words else "unknown"

        # Normalize for grouping
        normalized = normalize_for_grouping(family_name)

        groups[normalized].append(entry)

    return groups


def create_batches(surname_groups, batch_size=75):
    """
    Create batches from surname groups.
    Keep similar surnames together for efficient deduplication.

    Args:
        surname_groups: dict of {normalized_surname: [entries]}
        batch_size: target batch size (can be larger for efficiency)

    Returns:
        list of batches, each batch is a list of entries
    """
    batches = []
    current_batch = []

    # Sort groups by surname for consistency
    for surname, entries in sorted(surname_groups.items()):
        # If this group alone is too large, split it
        if len(entries) > batch_size:
            # Split large group into chunks
            for i in range(0, len(entries), batch_size):
                chunk = entries[i:i+batch_size]
                batches.append(chunk)
        elif len(current_batch) + len(entries) <= batch_size:
            # Add to current batch
            current_batch.extend(entries)
        else:
            # Current batch is full, start new batch
            if current_batch:
                batches.append(current_batch)
            current_batch = entries.copy()

    # Add final batch
    if current_batch:
        batches.append(current_batch)

    return batches


def merge_pass1_results():
    """
    Merge Pass 1 results with original entries.
    Returns combined list of all entries for Pass 2.
    """
    print("Loading original people entries...")
    with open(people_file, "r", encoding="utf-8") as f:
        original_entries = json.load(f)

    print(f"Loaded {len(original_entries)} original entries")

    # Check if Pass 1 results exist
    if not pass1_results_dir.exists():
        print("No Pass 1 results found, using only original entries")
        return original_entries

    # Load all Pass 1 results
    pass1_files = list(pass1_results_dir.glob("results_pass1_*.json"))

    if not pass1_files:
        print("No Pass 1 result files found, using only original entries")
        return original_entries

    print(f"Found {len(pass1_files)} Pass 1 result files")

    pass1_entries = []
    pass1_source_ids = set()

    for result_file in pass1_files:
        with open(result_file, "r", encoding="utf-8") as f:
            results = json.load(f)

            for entry in results:
                # Track which composite_ids came from Pass 1
                if "_source_custom_id" in entry:
                    pass1_source_ids.add(entry["_source_custom_id"])
                    # Remove internal tracking fields before adding
                    entry.pop("_source_custom_id", None)
                    entry.pop("_error", None)
                    entry.pop("_raw_content", None)

                pass1_entries.append(entry)

    print(f"Loaded {len(pass1_entries)} split entries from Pass 1")
    print(f"These came from {len(pass1_source_ids)} original multi-person entries")

    # Filter out original entries that were split in Pass 1
    filtered_original = [
        entry for entry in original_entries
        if entry["composite_id"] not in pass1_source_ids
    ]

    print(f"Filtered out {len(original_entries) - len(filtered_original)} original entries that were split")

    # Combine filtered original + Pass 1 splits
    combined = filtered_original + pass1_entries

    print(f"Total entries for Pass 2: {len(combined)}")

    return combined


def main():
    """
    Prepare batches for Pass 2: Deduplication and unified_id assignment.
    """
    print("=== Pass 2 Batch Preparation ===\n")

    # Merge Pass 1 results with original entries
    all_entries = merge_pass1_results()

    # Group by surname for efficient batching
    print("\nGrouping entries by surname...")
    surname_groups = group_people_by_surname(all_entries)

    print(f"Created {len(surname_groups)} surname groups")

    # Create batches
    print("\nCreating batches...")
    batches = create_batches(surname_groups, batch_size=75)

    print(f"Created {len(batches)} batches")

    # Create output directory
    batch_output_dir.mkdir(parents=True, exist_ok=True)

    # Save batches
    print("\nSaving batches...")
    for idx, batch in enumerate(batches, start=1):
        batch_file = batch_output_dir / f"batch_dedup_{idx:03d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"  Saved {batch_file.name} ({len(batch)} entries)")

    # Create summary log
    summary = {
        "total_entries": len(all_entries),
        "surname_groups": len(surname_groups),
        "batches_created": len(batches),
        "avg_batch_size": sum(len(b) for b in batches) / len(batches) if batches else 0,
        "output_directory": str(batch_output_dir)
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Summary log saved to {log_file}")
    print(f"✓ Batches ready for Pass 2 API processing!")
    print(f"\nSummary:")
    print(f"  Total entries: {summary['total_entries']}")
    print(f"  Batches: {summary['batches_created']}")
    print(f"  Avg batch size: {summary['avg_batch_size']:.1f}")


if __name__ == "__main__":
    main()
