import anthropic
from dotenv import load_dotenv
import json
from pathlib import Path
from datetime import datetime
import sys

load_dotenv()

client = anthropic.Anthropic()

project_root = Path(__file__).parent.parent

# ============================================================
# SYSTEM PROMPT — Operation A: Clean existing people
# ============================================================

CLEAN_SYSTEM_PROMPT = """
You are a specialized name parsing assistant. Your task is to parse existing person name data into a new, more precise schema.

CRITICAL OUTPUT REQUIREMENTS:
- Return ONLY a single valid JSON object matching the schema below
- No markdown code blocks, no explanations, no text outside the JSON

TASK:
Review the person entry and redistribute the name into the correct new fields. Also detect organisations that were not correctly flagged.

NEW SCHEMA FIELDS — read each definition carefully:
- name_prefix: Honorifics and titles that precede the given name (Prof., Dr., Lord, Count, General, Msgr., Abbé...). Extract from given_names or family_name if present there.
- name_particles: ONLY connective particles between family name and given name (von, van, de, del, della, di, du, d', le, la, des, zur, zum, ten, ter, af, av, auf der, van den...). Nothing else belongs here.
- name_suffix: Positional or honorific designations that follow the complete name ("Earl of Chesterfield", "Duke of Wellington", Jr., Sr., III, MBE...). Extract from given_names or family_name if present there.

FIELD RULES:
- family_name: surname only — no particles, no titles, no suffixes
- given_names: first and middle names only — no particles, no honorifics, no suffixes
- name_particles: ONLY the connective particle(s) — nothing else
- single_name: for organisations, single-word names, or names that cannot be split into family/given
- is_organisation: set true if the name clearly belongs to an institution, publisher, association, museum, collective, or any non-individual entity — even if the flag is currently false. When setting is_organisation to true: move the full name to single_name and set family_name and given_names to null.
- changes_made: true if you changed any field value from the input
- change_notes: brief explanation of what changed, null if changes_made is false

EXAMPLES:

Input: {"family_name": "Chesterfield", "given_names": "Philip Dormer Stanhope Earl of", "name_particles": null}
Output: {"family_name": "Chesterfield", "given_names": "Philip Dormer Stanhope", "name_prefix": null, "name_particles": null, "name_suffix": "Earl of", "single_name": null, "is_organisation": false, "changes_made": true, "change_notes": "Extracted 'Earl of' to name_suffix"}

Input: {"family_name": "Clausewitz", "given_names": "Karl von", "name_particles": null}
Output: {"family_name": "Clausewitz", "given_names": "Karl", "name_prefix": null, "name_particles": "von", "name_suffix": null, "single_name": null, "is_organisation": false, "changes_made": true, "change_notes": "Moved 'von' from given_names to name_particles"}

Input: {"family_name": "Bundesverlag", "given_names": "Österreichischer", "name_particles": null, "single_name": null, "is_organisation": false}
Output: {"family_name": null, "given_names": null, "name_prefix": null, "name_particles": null, "name_suffix": null, "single_name": "Österreichischer Bundesverlag", "is_organisation": true, "changes_made": true, "change_notes": "Name identifies an organisation; moved to single_name, set is_organisation true"}

Input: {"family_name": "Errington", "given_names": "Malcolm", "name_particles": null, "single_name": null, "is_organisation": false}
Output: {"family_name": "Errington", "given_names": "Malcolm", "name_prefix": null, "name_particles": null, "name_suffix": null, "single_name": null, "is_organisation": false, "changes_made": false, "change_notes": null}

OUTPUT SCHEMA (return exactly this structure):
{
    "person_id": integer (same as input),
    "unified_id": "string (same as input — do not change)",
    "family_name": "string or null",
    "given_names": "string or null",
    "name_prefix": "string or null",
    "name_particles": "string or null",
    "name_suffix": "string or null",
    "single_name": "string or null",
    "is_organisation": boolean,
    "changes_made": boolean,
    "change_notes": "string or null"
}

CRITICAL: Return ONLY the JSON object. No markdown blocks, no explanations.
"""

# ============================================================
# SYSTEM PROMPT — Operation B: Nopes dedup + clean
# ============================================================

NOPES_SYSTEM_PROMPT = """
You are a specialized name deduplication and cleaning assistant. For each nopes entry, you must:
1. Clean the name into the new schema fields
2. Check whether it matches an existing person in the context provided
3. Return either match identifiers (if found) or a cleaned new entry with a generated unified_id

CRITICAL OUTPUT REQUIREMENTS:
- Return ONLY a valid JSON array — exactly one object per nopes entry, in the same order
- No markdown code blocks, no explanations, no text outside the JSON

NAME SCHEMA FIELDS — same rules for all entries:
- family_name: surname only — no particles, no titles, no suffixes
- given_names: first and middle names only — no particles, no honorifics
- name_prefix: honorifics/titles before the given name (Prof., Dr., Lord, Count, Abbé, Msgr., General...)
- name_particles: ONLY connective particles (von, van, de, del, della, di, du, d', le, la, des, zur, zum, ten, ter, af, av...)
- name_suffix: positional/honorific suffixes ("Earl of Chesterfield", Jr., Sr., III...)
- single_name: for single-word names, pseudonyms, and organisations
- is_organisation: set true if name clearly belongs to a non-individual entity (institution, publisher, association, museum, collective...). When true: set family_name and given_names to null and use single_name for the full name.

PASS-THROUGH FIELDS — return exactly as received, do not alter:
- display_norm
- composite_id

MATCHING RULES:
Compare each nopes entry against the existing_people_context entries using these criteria:
- Same family_name (case-insensitive, diacritic-insensitive: ä=ae or a, ö=oe or o, ü=ue or u, ß=ss)
- Sufficiently similar given names: "Karl" matches "K.", "J.W." matches "Johann Wolfgang", initials match full names
- Particles must match or be clearly equivalent (von/v., de/d', van den/vanden)
- For organisations: match on single_name similarity
- When uncertain: do NOT match — it is always safer to create a new entry than to wrongly merge two people
- If a match is found: set match_found to true and populate matched_unified_id and matched_person_id. Set unified_id to null.
- If no match: set match_found to false, matched_unified_id and matched_person_id to null. Generate unified_id.

UNIFIED_ID GENERATION (for new entries only):
Format: lowercase, underscore-separated, no diacritics (ä→a, ö→o, ü→u, ß→ss, é→e, etc.)

For names with family_name + given_names:
- family_name part: lowercase family_name, remove diacritics
- given_names part (use CLEANED given_names, after extracting particles/suffixes):
  * Single alpha word: use as-is (e.g. "Karl" → "karl")
  * Multiple words: full first word + first letter of each subsequent word, joined by underscore
    "Johann Sebastian" → "johann_s"
    "Theodor W." → "theodor_w"
    "Marie-Henri" → "mariehenri" (hyphenated = single token)
- Final format: "{family_part}_{given_part}"
  Examples: "clausewitz_karl", "bach_johann_s", "adorno_theodor_w"

For single_name only (including organisations):
- Lowercase, replace spaces with underscore, remove diacritics
  "Voltaire" → "voltaire", "Österreichischer Bundesverlag" → "osterreichischer_bundesverlag"

If unable to determine: use "oops"

OUTPUT SCHEMA — one object per nopes entry:
{
    "display_norm": "string (pass through unchanged)",
    "composite_id": ["array", "pass", "through", "unchanged"],
    "family_name": "cleaned string or null",
    "given_names": "cleaned string or null",
    "name_prefix": "string or null",
    "name_particles": "string or null",
    "name_suffix": "string or null",
    "single_name": "string or null",
    "is_organisation": boolean,
    "match_found": boolean,
    "matched_unified_id": "string or null",
    "matched_person_id": integer or null,
    "unified_id": "generated string or null (null when match_found is true)"
}

CRITICAL: Return only the JSON array. No markdown blocks, no explanations.
"""


# ============================================================
# Submit functions
# ============================================================

def submit_clean_batch(batch_path):
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    print(f"Loaded {len(batch_data)} people from {batch_path.name}")

    requests = []
    for person in batch_data:
        request = {
            "custom_id": str(person["person_id"]),
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "temperature": 0,
                "system": [
                    {
                        "type": "text",
                        "text": CLEAN_SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": f"CLEAN TO JSON ONLY. No explanations, no markdown.\n\n{json.dumps(person, ensure_ascii=False)}"
                    }
                ]
            }
        }
        requests.append(request)

    print(f"Built {len(requests)} requests")

    message_batch = client.messages.batches.create(requests=requests)
    print(f"Batch submitted! ID: {message_batch.id}")

    return {
        "batch_id": message_batch.id,
        "status": "submitted",
        "file_path": str(batch_path),
        "entry_count": len(batch_data),
        "pass_type": "clean"
    }


def submit_nopes_batch(batch_path):
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    nopes_count = len(batch_data["nopes_entries"])
    context_count = len(batch_data["existing_people_context"])
    print(f"Loaded {nopes_count} nopes + {context_count} context from {batch_path.name}")

    batch_name = batch_path.stem

    user_message = f"""CLEAN AND DEDUPLICATE TO JSON ARRAY ONLY. No explanations, no markdown.

NOPES ENTRIES (process these — return exactly one object per entry, in order):
{json.dumps(batch_data["nopes_entries"], ensure_ascii=False, indent=2)}

EXISTING PEOPLE CONTEXT (use for comparison only — do NOT include in output):
{json.dumps(batch_data["existing_people_context"], ensure_ascii=False, indent=2)}
"""

    request = {
        "custom_id": batch_name,
        "params": {
            "model": "claude-sonnet-4-6",
            "max_tokens": 12000,
            "temperature": 0,
            "system": [
                {
                    "type": "text",
                    "text": NOPES_SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    }

    message_batch = client.messages.batches.create(requests=[request])
    print(f"Batch submitted! ID: {message_batch.id}")

    return {
        "batch_id": message_batch.id,
        "status": "submitted",
        "file_path": str(batch_path),
        "entry_count": nopes_count,
        "pass_type": "nopes"
    }


# ============================================================
# Main
# ============================================================

def main():
    """
    Submit batches for Operation A (clean) or Operation B (nopes).
    Usage:
        python people_clean_processor.py clean   # Submit clean batches
        python people_clean_processor.py nopes   # Submit nopes batches
    """
    if len(sys.argv) < 2:
        print("Usage: python people_clean_processor.py [clean|nopes]")
        print("  clean: Submit Operation A batches (clean existing 7817 people)")
        print("  nopes: Submit Operation B batches (nopes dedup + clean)")
        return

    pass_type = sys.argv[1].lower()

    if pass_type == "clean":
        batch_dir = project_root / "database/in_progress/clean_batches"
        tracking_file = project_root / "database/in_progress/clean_batch_tracking.json"
        batch_pattern = "batch_clean_*.json"
        submit_func = submit_clean_batch
        pass_name = "Operation A (clean existing people)"
    elif pass_type == "nopes":
        batch_dir = project_root / "database/in_progress/nopes_batches"
        tracking_file = project_root / "database/in_progress/nopes_batch_tracking.json"
        batch_pattern = "batch_nopes_*.json"
        submit_func = submit_nopes_batch
        pass_name = "Operation B (nopes dedup + clean)"
    else:
        print(f"Unknown pass type: {pass_type}")
        print("Use 'clean' or 'nopes'")
        return

    print(f"=== {pass_name} ===\n")

    batch_files = sorted(batch_dir.glob(batch_pattern))

    if not batch_files:
        print(f"No batch files found in {batch_dir}")
        print(f"Run the prep script first.")
        return

    print(f"Found {len(batch_files)} batch files")

    if tracking_file.exists():
        with open(tracking_file, "r") as f:
            tracking_data = json.load(f)
        print(f"Loaded existing tracking data ({len(tracking_data)} batches already submitted)")
    else:
        tracking_data = []

    submitted_files = {batch["file_path"] for batch in tracking_data}

    for batch_file in batch_files:
        if str(batch_file) in submitted_files:
            print(f"Skipping {batch_file.name} (already submitted)")
            continue

        print(f"\nProcessing {batch_file.name}...")
        result = submit_func(batch_file)
        result["submitted_at"] = datetime.now().isoformat()

        tracking_data.append(result)

        with open(tracking_file, "w") as f:
            json.dump(tracking_data, f, ensure_ascii=False, indent=2)

        print(f"Added to tracking file")

    print(f"\nDone! Total batches tracked: {len(tracking_data)}")


if __name__ == "__main__":
    main()
