import anthropic
from dotenv import load_dotenv
import json
from pathlib import Path
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

# Create connection to API
client = anthropic.Anthropic()

def submit_pass1_batch(batch_path):
    """
    Submit Pass 1 batch for splitting multi-person entries.
    """
    # Read the batch file
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    print(f"Loaded {len(batch_data)} entries from {batch_path}")

    # Create system prompt for Pass 1: Splitting multi-person entries
    system_prompt = """
    You are a specialized person name parsing assistant. Your task is to split entries containing multiple people into separate person records.

    CRITICAL OUTPUT REQUIREMENTS:
    - Return ONLY valid JSON array matching the exact schema provided
    - Never include markdown code blocks, explanations, or any text outside the JSON
    - Each input entry may produce 1 or more output entries
    - If you cannot parse an entry correctly, return it with unified_id="oops"

    INPUT STRUCTURE:
    You will receive person entries with these fields:
    {
        "book_id": "uuid",
        "composite_id": "string",
        "source_filename": "string",
        "display_name": "string containing multiple people",
        "family_name": null,
        "given_names": null,
        "name_particles": null,
        "single_name": "string containing multiple people",
        "is_author": boolean,
        "is_editor": boolean,
        "is_contributor": boolean,
        "is_translator": boolean,
        "sort_order": 0
    }

    OUTPUT STRUCTURE - Return an ARRAY of person objects:
    [
        {
            "book_id": "same as input",
            "composite_id": "same as input",
            "source_filename": "same as input",
            "display_name": "First Person Name",
            "family_name": "Surname",
            "given_names": "Given names",
            "name_particles": "von/van/de etc or null",
            "single_name": null,
            "is_author": same as input,
            "is_editor": same as input,
            "is_contributor": same as input,
            "is_translator": same as input,
            "sort_order": 1
        },
        {
            "book_id": "same as input",
            "composite_id": "same as input",
            "source_filename": "same as input",
            "display_name": "Second Person Name",
            "family_name": "Surname",
            "given_names": "Given names",
            "name_particles": null,
            "single_name": null,
            "is_author": same as input,
            "is_editor": same as input,
            "is_contributor": same as input,
            "is_translator": same as input,
            "sort_order": 2
        }
    ]

    CRITICAL PARSING RULES:
    1. SPLIT on: " und " (German "and") or " u. " (abbreviated "and")
    2. SORT_ORDER: Starts at 1 (not 0) and follows left-to-right appearance in string
    3. PRESERVE: book_id, composite_id, source_filename, all is_* flags EXACTLY as input
    4. NAME PARSING:
       - Parse each person into family_name and given_names
       - German format is often "Surname, Given" or "Given Surname"
       - Detect name_particles: von, van, de, della, etc.
       - Set single_name to null after parsing
    5. DISPLAY_NAME: Create proper display format for each person
    6. ERROR HANDLING: If you cannot determine the correct number of people or parse names correctly, return SINGLE entry with unified_id="oops"

    EXAMPLES:

    Input: "Klaus Berger und Christiane Nord"
    Output:
    [
        {
            ...(preserve book_id, composite_id, source_filename, is_* flags)...,
            "display_name": "Berger, Klaus",
            "family_name": "Berger",
            "given_names": "Klaus",
            "name_particles": null,
            "single_name": null,
            "sort_order": 1
        },
        {
            ...(same book metadata)...,
            "display_name": "Nord, Christiane",
            "family_name": "Nord",
            "given_names": "Christiane",
            "name_particles": null,
            "single_name": null,
            "sort_order": 2
        }
    ]

    Input: "Otto Abel u. Wilhelm Wattenbach"
    Output:
    [
        {
            "display_name": "Abel, Otto",
            "family_name": "Abel",
            "given_names": "Otto",
            "name_particles": null,
            "single_name": null,
            "sort_order": 1
        },
        {
            "display_name": "Wattenbach, Wilhelm",
            "family_name": "Wattenbach",
            "given_names": "Wilhelm",
            "name_particles": null,
            "single_name": null,
            "sort_order": 2
        }
    ]

    CRITICAL: Return only the JSON array. No explanations, no markdown blocks, no additional text.
    """

    # Build requests array for batch API
    requests = []
    for entry in batch_data:
        request = {
            "custom_id": entry["composite_id"],
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4000,
                "temperature": 0,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        CRITICAL: PARSE TO JSON ARRAY ONLY. No explanations, no markdown blocks.

                        ENTRY TO SPLIT:
                        {json.dumps(entry, ensure_ascii=False, indent=2)}
                        """
                    }
                ]
            }
        }
        requests.append(request)

    print(f"Built {len(requests)} requests")

    # Submit batch to API
    message_batch = client.messages.batches.create(requests=requests)
    print("Batch submitted!")
    print("Batch ID:", message_batch.id)

    return {
        "batch_id": message_batch.id,
        "status": "submitted",
        "file_path": str(batch_path),
        "entry_count": len(batch_data),
        "pass_type": "pass1_split"
    }


def submit_pass2_batch(batch_path):
    """
    Submit Pass 2 batch for deduplication and unified_id assignment.
    """
    # Read the batch file
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    print(f"Loaded {len(batch_data)} entries from {batch_path}")

    # Create system prompt for Pass 2: Deduplication
    system_prompt = """
    You are a specialized person deduplication assistant. Your task is to identify duplicate people entries and assign unified IDs and variant lists.

    CRITICAL OUTPUT REQUIREMENTS:
    - Return ONLY valid JSON array with ALL input entries
    - Never include markdown code blocks, explanations, or any text outside the JSON
    - Each entry MUST include: unified_id and variants fields
    - Preserve ALL original fields exactly as input

    INPUT: Array of person entries (may contain duplicates)
    OUTPUT: Same array with unified_id and variants added to each entry

    DEDUPLICATION LOGIC:
    1. GROUP similar entries (same person with variant spellings)
    2. GENERATE unified_id for each unique person (format: lowercase_surname_given_initial, e.g., "adorno_theodor_w")
    3. ASSIGN same unified_id to all variants of that person
    4. POPULATE variants array with OTHER display_name spellings (exclude current entry's display_name)

    UNIFIED_ID GENERATION:
    - Format: lowercase, underscore-separated
    - Use: family_name + given_names (first name + middle initial if present)
    - Example: "Adorno, Theodor W." → "adorno_theodor_w"
    - Example: "MOZART, Wolfgang Amadeus" → "mozart_wolfgang_a"
    - For organisations or single names → use normalized form
    - If cannot determine → unified_id="oops"

    VARIANTS ARRAY:
    - Include OTHER display_name values for this person
    - Exclude the current entry's own display_name
    - Examples:
      * Entry with display_name="ADORNO, Theodor W." → variants=["ADORNO, Th. W.", "Adorno, Theodor W."]
      * Entry with display_name="ADORNO, Th. W." → variants=["ADORNO, Theodor W.", "Adorno, Theodor W."]

    MATCHING CRITERIA (consider as same person):
    - Exact surname match with:
      * Given name variations (Theodor vs Th., Wolfgang vs W.)
      * Capitalization differences (ADORNO vs Adorno)
      * Punctuation/spacing variations
      * Full vs abbreviated middle names
    - Name particle handling (von, van, de should match)

    ERROR HANDLING:
    - If unsure if entries are the same person → give different unified_ids (safer to separate than merge incorrectly)
    - If entry has no usable name data → unified_id="oops", variants=[]

    OUTPUT STRUCTURE - Return array with EXACT input structure + 2 new fields:
    [
        {
            "book_id": "same as input",
            "composite_id": "same as input",
            "source_filename": "same as input",
            "display_name": "same as input",
            "family_name": "same as input",
            "given_names": "same as input",
            "name_particles": "same as input",
            "single_name": "same as input",
            "is_author": same as input,
            "is_editor": same as input,
            "is_contributor": same as input,
            "is_translator": same as input,
            "sort_order": same as input,
            "is_organisation": same as input (if present),
            "unified_id": "generated_id",
            "variants": ["other display_name values"]
        }
    ]

    EXAMPLE:

    Input:
    [
        {"display_name": "ADORNO, Theodor W.", "family_name": "ADORNO", "given_names": "Theodor W.", ...},
        {"display_name": "ADORNO, Th. W.", "family_name": "Adorno", "given_names": "Th. W.", ...},
        {"display_name": "Adorno, Theodor W.", "family_name": "Adorno", "given_names": "Theodor W.", ...},
        {"display_name": "MOZART, Wolfgang", "family_name": "Mozart", "given_names": "Wolfgang", ...}
    ]

    Output:
    [
        {
            "display_name": "ADORNO, Theodor W.",
            "family_name": "ADORNO",
            "given_names": "Theodor W.",
            ...(all other input fields)...,
            "unified_id": "adorno_theodor_w",
            "variants": ["ADORNO, Th. W.", "Adorno, Theodor W."]
        },
        {
            "display_name": "ADORNO, Th. W.",
            "family_name": "Adorno",
            "given_names": "Th. W.",
            ...(all other input fields)...,
            "unified_id": "adorno_theodor_w",
            "variants": ["ADORNO, Theodor W.", "Adorno, Theodor W."]
        },
        {
            "display_name": "Adorno, Theodor W.",
            "family_name": "Adorno",
            "given_names": "Theodor W.",
            ...(all other input fields)...,
            "unified_id": "adorno_theodor_w",
            "variants": ["ADORNO, Theodor W.", "ADORNO, Th. W."]
        },
        {
            "display_name": "MOZART, Wolfgang",
            "family_name": "Mozart",
            "given_names": "Wolfgang",
            ...(all other input fields)...,
            "unified_id": "mozart_wolfgang",
            "variants": []
        }
    ]

    CRITICAL: Return only the JSON array. No explanations, no markdown blocks, no additional text.
    """

    # Build requests array for batch API
    requests = []

    # For Pass 2, we submit the entire batch as one request
    request = {
        "custom_id": f"batch_{Path(batch_path).stem}",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 20000,
            "temperature": 0,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    CRITICAL: PARSE TO JSON ARRAY ONLY. No explanations, no markdown blocks.

                    ENTRIES TO DEDUPLICATE (return all with unified_id and variants added):
                    {json.dumps(batch_data, ensure_ascii=False, indent=2)}
                    """
                }
            ]
        }
    }
    requests.append(request)

    print(f"Built 1 request containing {len(batch_data)} entries")

    # Submit batch to API
    message_batch = client.messages.batches.create(requests=requests)
    print("Batch submitted!")
    print("Batch ID:", message_batch.id)

    return {
        "batch_id": message_batch.id,
        "status": "submitted",
        "file_path": str(batch_path),
        "entry_count": len(batch_data),
        "pass_type": "pass2_dedup"
    }


def main():
    """
    Process batches for Pass 1 or Pass 2.
    Usage:
        python people_batch_processor.py pass1  # Process Pass 1 (splitting)
        python people_batch_processor.py pass2  # Process Pass 2 (deduplication)
    """
    # Determine which pass to run
    if len(sys.argv) < 2:
        print("Usage: python people_batch_processor.py [pass1|pass2]")
        print("  pass1: Split multi-person entries")
        print("  pass2: Deduplicate and assign unified IDs")
        return

    pass_type = sys.argv[1].lower()

    if pass_type == "pass1":
        batch_dir = Path("database/in_progress/pass1_batches")
        tracking_file = Path("database/in_progress/pass1_batch_tracking.json")
        batch_pattern = "batch_split_*.json"
        submit_func = submit_pass1_batch
        pass_name = "Pass 1 (Splitting)"
    elif pass_type == "pass2":
        batch_dir = Path("database/in_progress/pass2_batches")
        tracking_file = Path("database/in_progress/pass2_batch_tracking.json")
        batch_pattern = "batch_dedup_*.json"
        submit_func = submit_pass2_batch
        pass_name = "Pass 2 (Deduplication)"
    else:
        print(f"Unknown pass type: {pass_type}")
        print("Use 'pass1' or 'pass2'")
        return

    print(f"=== {pass_name} ===\n")

    # Find all batch files
    batch_files = sorted(batch_dir.glob(batch_pattern))

    if not batch_files:
        print(f"No batch files found in {batch_dir}")
        return

    print(f"Found {len(batch_files)} batch files to process")

    # Load existing tracking data if it exists
    if tracking_file.exists():
        with open(tracking_file, "r") as f:
            tracking_data = json.load(f)
        print(f"Loaded existing tracking data with {len(tracking_data)} batches")
    else:
        tracking_data = []

    # Get already submitted batch IDs
    submitted_files = {batch["file_path"] for batch in tracking_data}

    # Process each batch
    for batch_file in batch_files:
        if str(batch_file) in submitted_files:
            print(f"Skipping {batch_file.name} (already submitted)")
            continue

        print(f"\nProcessing {batch_file.name}...")
        result = submit_func(batch_file)

        # Add timestamp
        result["submitted_at"] = datetime.now().isoformat()

        # Add to tracking
        tracking_data.append(result)

        # Save tracking file after each submission
        with open(tracking_file, "w") as f:
            json.dump(tracking_data, f, ensure_ascii=False, indent=2)

        print(f"Added {batch_file.name} to tracking file")

    print(f"\n✓ All batches submitted! Tracking saved to {tracking_file}")
    print(f"Total batches tracked: {len(tracking_data)}")


if __name__ == "__main__":
    main()
