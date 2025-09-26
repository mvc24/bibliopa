import ijson
from pathlib import Path
from pprint import pp
import re
import unicodedata

# corrupt_entries = Path("data/logs/corrupt_entries_log.json")
corrupt_entries = Path("test_entries.json")

test = "\"subtitle\": \"Allegorisches Zeitbild. Mit den Beigaben „Von mir über mich\", „Der Noeckergreis\" und Porträt\",\n  \"authors\": "

is_key = "(\\\"\w*\\\":)"

# q = re.sub("\"", "'", test)
# pp(q)


def clean_json():
    newline = "\n"

    with open(corrupt_entries, "r") as f:
        for entry in ijson.items(f, "item"):
            raw = entry["raw_response"]
            keys = re.findall(is_key, raw)



            # n = re.sub(newline, "", raw)
            # w = n.strip(" ")
            # w = re.sub('\s{2,}', "", n)

        pp(keys)
            # pp(raw)

clean_json()
