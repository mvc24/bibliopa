import anthropic
from dotenv import load_dotenv
import json
from pathlib import Path
from pprint import pp

# load function to get environment variables
load_dotenv()

# create connection to connect to API
client = anthropic.Anthropic()

def submit_batch(batch_path):

    # Read the sample entries file
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    print(f"Loaded {len(batch_data)} entries")
    print("First entry text:", batch_data[0]["text"])
    print("First entry composite_id:", batch_data[0]["composite_id"])

    # Create prompt message
    system_prompt = """
    You are a specialized bibliography parsing assistant. Your task is to convert German bibliographic entries into structured JSON data.

    CRITICAL OUTPUT REQUIREMENTS:
    - Return ONLY valid JSON matching the exact schema provided
    - Never include markdown code blocks, explanations, or any text outside the JSON
    - If you cannot parse an entry completely, still return valid JSON with null values for unknown fields
    - Always populate the "administrative.original_entry" field with the complete, unmodified input text

    BIBLIOGRAPHIC CONTEXT:
    These entries were catalogued by an octogenarian librarian using RAK (Regeln für die alphabetische Katalogisierung) format as base standard. Expect: punctuation inconsistencies, accents used as apostrophes, varying abbreviation styles, typos, and other age-related cataloging inconsistencies.

    CHARACTER ENCODING ISSUES:
    Fix common encoding problems: Ã¼→ü, Ãž→ß, Ã„→Ä, ÃƒÂ¼→ü, Ãƒâ€ž→Ä, etc.

    SCHEMA (return exactly this structure):
    {
        "identifier": null,
        "title": "string",
        "subtitle": "string",
        "authors": [{"display_name": "string", "family_name": "string", "given_names": "string", "name_particles": null, "single_name": null}],
        "editors": [/* same person structure */],
        "contributors": [/* same person structure */],
        "publisher": "string",
        "place_of_publication": "string",
        "publication_year": "integer",
        "edition": "string",
        "pages": "integer",
        "format_original": "string",
        "format_expanded": "string",
        "condition": "string",
        "copies": "integer",
        "illustrations": "string",
        "packaging": "string",
        "isbn": "string",
        "price": "integer",
        "topic": "string",
        "is_translation": "boolean",
        "original_language": "string",
        "translator": "person object or null",
        "is_multivolume": "boolean",
        "series_title": "string",
        "total_volumes": "integer",
        "volumes": [{"volume_number": "integer", "volume_title": "string", "pages": "integer", "notes": "string"}],
        "administrative": {
            "source_filename": "string",
            "original_entry": "string",
            "parsing_confidence": "high|medium|low",
            "needs_review": "boolean",
            "verification_notes": "string or null"
        }
    }

    PARSING RULES:
    1. USE PROVIDED VALUES: Always use the exact PRICE and TOPIC values provided in the user message
    2. GERMAN BIBLIOGRAPHIC ABBREVIATIONS: Extract and expand format abbreviations:
    - format_original: Copy the abbreviation exactly as written in the entry
    - format_expanded: Expand using standard German bibliographic terms
    - O + material patterns: OLn→Originalleinen, OBrosch→Originalbroschur, OPbd→Originalpappband
    - With additions: OLn.m.OU→"Originalleinen mit Originalumschlag"
    3. COPIES: "2 Ex." means copies=2, "3 Exemplare" means copies=3
    4. MULTIVOLUME DETECTION: "Band", "Bd.", "In X Bänden", numbered volumes, "Teil I/II"
    5. AUTHOR NAMES: Typically "SURNAME, Given Names" format in German cataloging
    6. PLACE BEFORE PUBLISHER: German cataloging puts place of publication before publisher
    7. CROSS-REFERENCES: Entries containing "Siehe..." should have parsing_confidence="low", needs_review=true
    8. TRANSLATION INDICATORS: "A.d." (Aus dem), "Übersetzt von", "Deutsch von", "Übertragen von", etc.

    CONFIDENCE LEVELS:
    - "high": Clean, complete entries with all major fields identifiable
    - "medium": Minor formatting issues, some unclear abbreviations, or missing non-critical data
    - "low": Cross-references, significant structural problems, or major missing data

    VERIFICATION USING BOOK KNOWLEDGE:
    Compare parsed author names, titles, and publishers against your knowledge of books and flag potential issues in verification_notes:
    - Misspelled author names (e.g., "Shakespear" vs "Shakespeare")
    - Unusual publisher names that don't match known German publishers
    - Title variations that might indicate typos
    - Publication years that seem inconsistent with known works
    - Use null for verification_notes when no issues are detected

    CRITICAL: Return only the JSON object. No explanations, no markdown blocks, no additional text.
    """


    # Build requests array for batch API
    requests = []
    for entry in batch_data:
        request = {
            "custom_id": entry["composite_id"],
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 8000,
                "temperature": 0,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        CRITICAL: PARSE TO JSON ONLY. No explanations, no markdown blocks.

                        PRICE: {entry["price"]}
                        TOPIC: {entry["topic"]}
                        ENTRY: {entry["text"]}
                        """

                    }
                ]
            }
        }
        requests.append(request)

    print(f"Built {len(requests)} requests")
    print("First request custom_id:", requests[0]["custom_id"])
    # print("First request content preview:", requests[0]["params"]["messages"][0]["content"][:200])

# Submit batch to API
    message_batch = client.messages.batches.create(requests=requests)
    print("Batch submitted!")
    print("Batch ID:", message_batch.id)

    return {
        "batch_id": message_batch.id,
        "status": "submitted",
        "file_path": str(batch_path),
        "entry_count": len(batch_data)
    }
