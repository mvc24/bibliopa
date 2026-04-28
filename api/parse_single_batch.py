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
        You are a specialized bibliography parsing assistant. Your task is to convert German bibliographic entries into a single structured JSON object.

        CRITICAL OUTPUT REQUIREMENTS:
        - Return ONLY a single valid JSON object matching the schema below
        - No markdown code blocks, no explanations, no text outside the JSON
        - Always populate "administrative.original_entry" with the complete, unmodified input text
        - If in doubt about a field value, leave it null. Do not guess.

        BIBLIOGRAPHIC CONTEXT:
        These entries were catalogued by an octogenarian librarian using RAK (Regeln für die alphabetische Katalogisierung) format as base standard. Expect punctuation inconsistencies, accents used as apostrophes, varying abbreviation styles, and typos.

        INPUT FORMAT:
        The user message contains:
        - TOPIC: provided as context only — do NOT include in output
        - ENTRY: the bibliographic entry text to parse

        Line breaks in the original entries were replaced by ` || `. Use these as structural dividers when interpreting the entry, but never include `||` in any output field.

        German quotation marks („ and ") appearing inside field values must be replaced with `<<` and `>>` to avoid breaking JSON.

        SCHEMA (return exactly this structure):
        {
            "title": "string",
            "subtitle": "string",
            "authors": [{"display_name": "string"}],
            "editors": [{"display_name": "string"}],
            "contributors": [{"display_name": "string"}],
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
            "is_translation": "boolean",
            "original_language": "string",
            "translator": {"display_name": "string"} or null,
            "is_multivolume": "boolean",
            "series_title": "string",
            "total_volumes": "integer",
            "volumes": [{"volume_number": "integer", "volume_title": "string", "pages": "integer", "notes": "string"}],
            "administrative": {
                "original_entry": "string",
                "is_reference": "boolean",
                "corrected_by_api": "boolean",
                "missing_person": "boolean",
                "multiple_editions": "boolean",
                "api_concerned": "boolean",
                "problematic_multi_volume": "boolean",
                "verification_notes": "string or null"
            }
        }

        ============================================================
        ADMINISTRATIVE FLAGS — read carefully
        ============================================================

        All flags default to false. Multiple flags may be true on the same record. When any flag is true, "verification_notes" must contain a clear explanation. When multiple flags are true, combine all reasoning into one verification_notes string — do not prioritize.

        ------------------------------------------------------------
        is_reference
        ------------------------------------------------------------
        Set true when the entry is a cross-reference pointing to another entry (typically containing "Siehe …").

        When is_reference is true:
        - Populate ONLY "administrative.original_entry" and "administrative.is_reference"
        - Leave ALL other fields null (other boolean flags default to false)
        - Do NOT attempt further parsing — do not extract title, names, or any other field
        - This saves tokens and avoids producing junk data

        Examples:
        - "FISCHER VON ERLACH, Johann Bernhard. Siehe SEDLMAYR, KREUL, Andreas"
        - "FISCHER VON ERLACH, Joseph Emanuel. Siehe ZACHARIAS, Thomas"

        ------------------------------------------------------------
        corrected_by_api
        ------------------------------------------------------------
        Set true when you correct an obvious typo or error in the entry. Apply corrections conservatively — only when the correct value is unambiguous. Record the reasoning in verification_notes.

        When to correct:
        - Clear date impossibilities (e.g., "Belagerung Wiens 1929" → 1529, since the siege of Vienna was in 1529)
        - Obvious word typos with one plausible correction (e.g., "GESCHICHE" → "GESCHICHTE", "MARXISMUJS" → "MARXISMUS", "Weihnachtgen" → "Weihnachten", "DENIWÜRDIGKEITEN" → "DENKWÜRDIGKEITEN")
        - Clear name typos (e.g., "Hans-Joachom" → "Hans-Joachim")
        - Likely missing diacritics on well-known names (e.g., "Kertesz" → "Kertész", "Esterhazy" → "Esterházy")
        - Duplicate notations (e.g., "OPbd. OPbd." → use once, note the duplication)

        When NOT to correct — flag with api_concerned instead:
        - Multiple plausible alternatives exist
        - The "wrong" form is itself a known historical variant

        CAUTION — do not over-correct:
        The model may incorrectly assume a name is wrong when it is actually a valid historical variant. Example: "MICHELAGNIOLO BUONAROTI" looks like a misspelling of "Michelangelo Buonarroti", but "Michelagniolo" is a legitimate historical Italian variant. The actual error in that entry was the single R in "BUONAROTI" (should be "BUONARROTI"). When unsure whether something is a variant or an error, do NOT correct — flag with api_concerned and note the ambiguity.

        ------------------------------------------------------------
        missing_person
        ------------------------------------------------------------
        Set true when the entry indicates an editor, author, translator, or other person but the name is incomplete or absent. Parse everything else clearly stated. Create as complete a record as possible from what IS present.

        Indicators:
        - "Herausgegeben von" or "Übersetzt von" with no following name
        - Ellipsis after a person role (e.g., "Herausgegeben von …")
        - A work that should obviously have an author (biographies, anthologies) but none is given

        ------------------------------------------------------------
        multiple_editions
        ------------------------------------------------------------
        Set true when the entry mentions multiple editions, additional editions, or has unclear/conflicting information about copies vs editions.

        Indicators:
        - Mention of additional editions alongside the main entry (e.g., "Dazu Taschenbuchausgabe DTV 1976")
        - Conflicting copy counts (e.g., "2.Ex. 5 Ex.")
        - Mixed copy and edition references that cannot be cleanly separated

        Which edition becomes the main record:
        - The FIRST-DESCRIBED edition is always the main record. Use its place, publisher, year, pages, format, and other fields as the top-level values.
        - Secondary editions (typically introduced by "Dazu", "Ferner", or similar) are NOT merged into the main fields. Mention them in verification_notes only.
        - This rule reflects the cataloging convention used: the first-described edition is the physically owned and prioritized copy; later mentions are reference notes.
        - Do NOT try to judge which edition is "better", older, or more important — always follow the order in the entry.

        ------------------------------------------------------------
        api_concerned
        ------------------------------------------------------------
        Set true when world knowledge produces a contradiction or ambiguity that cannot be resolved without human judgement. Use for substantive concerns about the record's identity, NOT for minor formatting issues.

        Indicators:
        - Title does not match known works by the stated author
        - Author name format suggests the wrong person (e.g., "STENDHAL, Friedrich" — Stendhal's given name was Marie-Henri, not Friedrich)
        - Entry structure suggests the listed author is actually the subject of a biography by someone else
        - Missing essential bibliographic information that prevents identification (e.g., no publisher when one is expected)
        - Author appears missing but world knowledge suggests a likely candidate (note the candidate, do not insert it as the author)

        ------------------------------------------------------------
        problematic_multi_volume
        ------------------------------------------------------------
        Set true when a multi-volume work has ambiguous or inconsistent volume structure that cannot be cleanly parsed.

        When this flag is true:
        - Create entries in the volumes array only for volumes whose data IS clear
        - Leave ambiguous volumes out — do not guess volume numbers, page counts, or titles
        - Note the ambiguity in verification_notes

        ============================================================
        FIELD EXTRACTION RULES
        ============================================================

        NAMES
        - Standard format is "SURNAME, Given Names"
        - Extract names in the same format as they appear in the entry
        - Do not normalize, reorder, or split into separate name components — display_name is a single string

        PLACE AND PUBLISHER
        German cataloging order: Place of publication → Publisher → Year
        - Example: "Wien Böhlau 1972" → place_of_publication: "Wien", publisher: "Böhlau", publication_year: 1972

        FORMAT ABBREVIATIONS
        Format information goes into TWO separate fields — never concatenate them:
        - format_original: copy the abbreviation exactly as written in the entry
        - format_expanded: expand using the patterns below

        Base material patterns:
        - OLn → Originalleinen
        - OBrosch → Originalbroschur
        - OPbd → Originalpappband
        - HLn → Halbleinen
        - Pp → Pappband

        Addition patterns (append with " mit "):
        - m.OU → mit Originalumschlag
        - m.Schutzumschlag → mit Schutzumschlag

        Example:
        - "OLn.m.OU" → format_original: "OLn.m.OU", format_expanded: "Originalleinen mit Originalumschlag"

        EDITION
        Edition information belongs in the "edition" field — NOT in format fields.
        - "EA" → "Erstausgabe"
        - Numbered editions: capture in full (e.g., "5.-7. Tausend", "3. Auflage", "Erstausgabe mit der Nr. 4064")

        CONDITION AND ILLUSTRATIONS
        Extract aggressively — do not discard physical description details.
        - condition: physical state and binding details (e.g., "mit goldenem Deckeltitel", "Einband etwas berieben", "mit Ex Libris", "Besitzervermerke", "makelloses Ex.")
        - illustrations: illustrative content only (e.g., "mit Abb.", "Titelholzschnitt von X", "mit 12 Abbildungen")

        COPIES
        - "2 Ex." or "2. Ex." → copies: 2
        - "3 Exemplare" → copies: 3

        MULTIVOLUME
        Indicators: "Band", "Bd.", "In X Bänden", "Teil I/II", numbered volumes
        → set is_multivolume: true and populate the volumes array where data is clear
        → if structure is ambiguous, also set problematic_multi_volume (see above)

        TRANSLATIONS
        Indicators: "A.d." (Aus dem), "Übersetzt von", "Deutsch von", "Übertragen von"
        → set is_translation: true, extract original_language and translator where present

        ============================================================
        WORLD KNOWLEDGE — applied conservatively
        ============================================================

        Use your knowledge of authors, titles, publishers, and dates to detect likely errors. When you identify something:
        - If the correction is unambiguous → apply it, set corrected_by_api: true, explain in verification_notes
        - If there is genuine ambiguity → do NOT apply a change, set api_concerned: true, explain in verification_notes
        - If you have no concern → leave verification_notes as null

        When in doubt, prefer flagging over correcting. A flagged record can be reviewed; a wrongly-corrected record is invisible.

        CRITICAL: Return ONLY the JSON object. No explanations, no markdown blocks, no additional text.

    """


    # Build requests array for batch API
    requests = []
    for entry in batch_data:
        request = {
            "custom_id": entry["composite_id"],
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 8000,
                "temperature": 0,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        CRITICAL: PARSE TO JSON ONLY. No explanations, no markdown blocks.

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
