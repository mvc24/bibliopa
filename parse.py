import anthropic
from dotenv import load_dotenv
from datetime import datetime
import json

# load function to get environment variables
load_dotenv()

# create connection to connect to API
client = anthropic.Anthropic()

# Read the sample entries file
with open('data/sample_entries.txt', 'r', encoding='utf-8') as file:
    sample_entries = file.read()

# Create prompt message

prompt = f"""
Parse the bibliography entries below and return detailed JSON.
For each entry, extract:

- authors: array of objects with "first_name" and "last_name" (empty array if no authors)
- title: exact title as written
- publisher: publisher name
- location: publication location
- year: publication year
- price: price if listed, null if not
- pages: number of pages if mentioned, null if not
- condition: condition description as written in German
- notes: any additional details (illustrations, maps, etc.) as written in German
- is_multivolume: true/false
- is_edited: true/false
- volumes: array of volume information if multivolume (empty array if single volume)

for edited works, do the following:
- is_edited: true
- authors: empty array
- editors: empty array
- contributors: array with all the names mentioned

Keep all German text exactly as written - do not translate anything.

Here are the entries to parse:

{sample_entries}
"""

# call API, parse sample file


#"""
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=20000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
)
#"""

response_dict = response.model_dump()

# create information for file path
timestamp = datetime.now().strftime("%Y%m%d-%H%M")
label = input("Enter label:")
filepath =f"data/parsed/{label}-{timestamp}.json"

# create new file with entire parsing result including metadata

with open(filepath, "x") as parsedfile:
    json.dump(response_dict, parsedfile, ensure_ascii= False, indent=2)

"""with open(filepath, "x") as parsedfile:
    parsedfile.write(response)"""
