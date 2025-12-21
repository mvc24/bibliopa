"""
Repair corrupted person records from oops.json.

This script extracts valid JSON data from the _raw_content field of entries
where parsing initially failed. Each wrapper entry contains an array of person
records that need to be extracted, enriched with lineage tracking, and written
to a clean output file.
"""

import json
import re
from pathlib import Path


def clean_raw_content(raw_content: str) -> str:
    """
    Extract a JSON array from the _raw_content blob.

    Strips markdown code fences, trims leading noise before the array,
    and greedily decodes objects to drop any truncated tail.
    """
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE).strip()

    start_idx = content.find("[")
    if start_idx == -1:
        raise ValueError("No JSON array found in _raw_content")

    content = content[start_idx:]

    try:
        json.loads(content)
        return content
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    items = []
    idx = 1  # Skip initial '['
    length = len(content)

    while idx < length:
        while idx < length and content[idx] in " \t\r\n,":
            idx += 1

        if idx >= length or content[idx] == "]":
            break

        try:
            obj, next_idx = decoder.raw_decode(content, idx)
        except json.JSONDecodeError:
            break

        items.append(obj)
        idx = next_idx

    if not items:
        raise ValueError("Unable to extract JSON objects from _raw_content")

    return json.dumps(items, ensure_ascii=False)


def repair_oops_json(input_path: Path) -> dict:
    """
    Repair corrupted person records from oops.json.

    Reads entries with unified_id == "oops", parses the _raw_content field,
    and extracts all person records while preserving lineage tracking.

    Args:
        input_path: Path to oops.json file

    Returns:
        Dictionary with processing statistics:
        {
            "success": bool,
            "entries_processed": int,
            "persons_extracted": int,
            "failed": int,
            "output_file": str
        }
    """
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load corrupted data
    with open(input_path, "r", encoding="utf-8") as f:
        oops_entries = json.load(f)

    cleaned_persons = []
    failed_repairs = []
    entries_processed = 0

    print("Processing oops.json corruption repair...")

    for entry in oops_entries:
        # Verify this is an error wrapper entry
        if entry.get("unified_id") != "oops":
            print(f"⚠️  Warning: Unexpected entry with unified_id={entry.get('unified_id')}, skipping")
            continue

        entries_processed += 1
        source_custom_id = entry.get("_source_custom_id", "unknown")
        raw_content = entry.get("_raw_content", "")

        if not raw_content:
            failed_repairs.append({
                "_source_custom_id": source_custom_id,
                "error": "Empty _raw_content field",
                "raw_snippet": ""
            })
            continue

        try:
            # Clean and parse the raw content
            cleaned_content = clean_raw_content(raw_content)
            persons_array = json.loads(cleaned_content)

            # Validate it's an array
            if not isinstance(persons_array, list):
                raise ValueError(f"Expected array, got {type(persons_array).__name__}")

            # Enrich each person record with source tracking
            for person in persons_array:
                person["_source_custom_id"] = source_custom_id
                cleaned_persons.append(person)

        except (json.JSONDecodeError, ValueError) as e:
            # Log parsing failure and continue
            failed_repairs.append({
                "_source_custom_id": source_custom_id,
                "error": str(e),
                "raw_snippet": raw_content[:200] + "..." if len(raw_content) > 200 else raw_content
            })
            continue

    # Write cleaned output
    output_dir = input_path.parent
    output_path = output_dir / "oops_cleaned.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_persons, f, ensure_ascii=False, indent=2)

    # Write error log if there were failures
    if failed_repairs:
        error_path = output_dir / "oops_repair_errors.json"
        with open(error_path, "w", encoding="utf-8") as f:
            json.dump(failed_repairs, f, ensure_ascii=False, indent=2)

    # Print summary report
    print(f"✓ Successfully processed: {entries_processed} wrapper entries")
    print(f"✓ Total person records extracted: {len(cleaned_persons)}")
    print(f"✗ Failed to parse: {len(failed_repairs)} entries")
    print(f"Output written to: {output_path}")

    if failed_repairs:
        print(f"⚠️  Error log written to: {error_path}")

    return {
        "success": len(failed_repairs) == 0,
        "entries_processed": entries_processed,
        "persons_extracted": len(cleaned_persons),
        "failed": len(failed_repairs),
        "output_file": str(output_path)
    }


if __name__ == "__main__":
    # Default paths
    base_dir = Path(__file__).parent.parent
    oops_file = base_dir / "database" / "in_progress" / "oops.json"

    result = repair_oops_json(oops_file)

    if result["success"]:
        print("\n✅ All entries successfully repaired!")
    else:
        print(f"\n⚠️  {result['failed']} entries failed - check error log for details")
