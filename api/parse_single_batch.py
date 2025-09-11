import anthropic
from dotenv import load_dotenv
from datetime import datetime
import json
from pathlib import Path
from pprint import pp

# load function to get environment variables
load_dotenv()

# create connection to connect to API
client = anthropic.Anthropic()
files = Path("data/batched")

sample = Path("data/batched/symbolkunde/symbolkunde_2-2.json")


# Read the sample entries file
with open(sample, 'r', encoding='utf-8') as f:
    test_file = json.load(f)

print(f"Loaded {len(test_file)} entries")
print("First entry text:", test_file[0]['text'])
print("First entry composite_id:", test_file[0]['composite_id'])

# Create prompt message
prompt = """
CONTEXT:
These entries were catalogued by an octogenarian librarian using RAK (Regeln für die alphabetische Katalogisierung) format as base standard. Watch for: punctuation inconsistencies, accents used as apostrophes, varying abbreviation styles, typos.

SCHEMA:

{
    "identifier": null,
    "title": "string",
    "subtitle": "string",
    "authors": [
        {
            "display_name": "Churchill, Winston C.",
            "family_name": "Churchill",
            "given_names": "Winston C.",
            "name_particles": null,
            "single_name": null
        }
    ],
    "editors": [ /* same person structure */],
    "contributors": [ /* same person structure */],
    "publisher": "string",
    "place_of_publication": "string",
    "publication_year": "integer",
    "edition": "string", // "Zweite Auflage", "Erstausgabe"
    "pages": "integer",
    "format_original": "string", // "OBrosch.", "OLn.m.OU"
    "format_expanded": "string", // "Original-Broschur", "Original-Leinen mit Original-Umschlag"
    "condition": "string", // "Sehr gut erhalten", "Neuwertig"
    "copies": "integer", // "2 Ex."
    "illustrations": "string", // "Mit 27 Abb. und 19 Karten"
    "packaging": "string", // "In Original-Kassette"
    "isbn": "string",
    "price": "integer", // 30, 40, null
    "topic": "string", // One of your theme categories
    "is_translation": "boolean",
    "original_language": "string", // null if not translation
    "translator": "person object", // null if not translation
    "is_multivolume": "boolean",
    "series_title": "string", // null if single volume
    "total_volumes": "integer", // null if single volume
    "volumes": [
        {
            "volume_number": "integer",
            "volume_title": "string",
            "pages": "integer",
            "notes": "string" // "Mit 27 Abb. und 19 Karten"
        }
    ],
    "administrative": {
        "source_filename": "string", // "PHILOSOPHIE.docx"
        "original_entry": "string", // Complete original text
        "parsing_confidence": "high|medium|low",
        "needs_review": "boolean"
    }
}


PARSING INSTRUCTIONS:
- Use provided EXTRACTED PRICE value for price field
- Use provided TOPIC value for topic field
- Handle character encoding issues (Ã„=Ä, Ã¼=ü, etc.) - decode properly in output
- Recognize German bibliographic abbreviations: EA=Erstausgabe, OLn=Original-Leinen, OU=Original-Umschlag, TB=Taschenbuch, etc.

- Identify copies: "2 Ex." means copies=2
- Handle cross-references: entries like "Siehe..." should have parsing_confidence="low", needs_review=true
- Author names: Last name typically appears first, followed by given names
- Missing information: use null for absent fields, don't guess
- Multivolume works: look for numbered volumes (1. Band, 2. Band, etc.)
- Format expansion: OBrosch.=Original-Broschur, OLn.m.OU=Original-Leinen mit Original-Umschlag
- Always populate administrative.original_entry with complete input text
- Set parsing_confidence: "high" for clear entries, "medium" for minor issues, "low" for unclear/cross-reference entries
- Place of publication comes before publisher in German cataloging

OUTPUT: Return valid JSON matching the schema. Preserve all German text exactly as written.

Here are the entries to parse:


"""


# Build requests array for batch API
requests = []
for entry in test_file:
    request = {
        "custom_id": entry['composite_id'],
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 8000,
            "messages": [
                {
                    "role": "user",
                    "content": f"""Parse this bibliography entry into structured JSON.

                    EXTRACTED PRICE: {entry['price']}
                    TOPIC: {entry['topic']}

                    ENTRY TEXT: {entry['text']}

                    {prompt}"""

                }
            ]
        }
    }
    requests.append(request)

print(f"Built {len(requests)} requests")
print("First request custom_id:", requests[0]['custom_id'])
# print("First request content preview:", requests[0]['params']['messages'][0]['content'][:200])



# Submit batch to API
# message_batch = client.messages.batches.create(requests=requests)
# print("Batch submitted!")
# print("Batch ID:", message_batch.id)
# print("Batch status:", message_batch.processing_status)

batch_id = "msgbatch_012zLTg5QEkhgppuGDz3uEM5"

# Check batch status
batch_status = client.messages.batches.retrieve(batch_id)
print("Current status:", batch_status.processing_status)

# Get results (when status is "ended")
batch_results = client.messages.batches.results(batch_id)
print("Results ready!")

# Get batch results
batch_results = client.messages.batches.results(batch_id)
print("Retrieved results!")

# Reset the iterator if needed (since we just consumed it with len())
batch_results = client.messages.batches.results(batch_id)

# DEBUG: Look at the first result structure
results_list = list(batch_results)
print(f"Number of results in list: {len(results_list)}")
# Convert results to JSON-serializable format
results_data = []
for result in results_list:  # Use the list we already created
    if result.result and result.result.type == "succeeded":  # Changed from "message" to "succeeded"
        # Extract the text content from the message
        response_text = result.result.message.content[0].text  # Changed path

        # Strip markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json\n", "").replace("\n```", "")

        try:
            # Parse the actual JSON
            parsed_json = json.loads(response_text)
            result_data = {
                "custom_id": result.custom_id,
                "parsed_entry": parsed_json
            }
        except json.JSONDecodeError as e:
            result_data = {
                "custom_id": result.custom_id,
                "error": f"JSON parsing failed: {e}",
                "raw_response": response_text
            }

        results_data.append(result_data)

# Save results to file (single file creation)
timestamp = datetime.now().strftime("%Y%m%d-%H%M")
filepath = f"data/parsed/batch_symbolkunde_test_{timestamp}.json"

with open(filepath, "w", encoding='utf-8') as f:
    json.dump(results_data, f, ensure_ascii=False, indent=2)

print(f"Results saved to: {filepath}")
print(f"Number of results: {len(results_data)}")
