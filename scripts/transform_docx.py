from rich import print as rprint
from rich import inspect
import json
import re
from datetime import datetime
from pathlib import Path
from docx import Document
from datetime import datetime
import os
import unicodedata


folder_prepped = Path("data/raw/prepped")
originals_dir = Path("data/raw/original")
processing_log = Path("data/logs/processing_log.json")

def get_paths():
    paths = []
    for file in originals_dir.iterdir():
        paths.append(file)
    paths.sort()
    # rprint(paths)
    return paths

# get_paths()
paths = get_paths()

def read_entries():

    for path in paths:
        if not path.exists():
            raise FileNotFoundError("File doesn't exist")

        entries = []
        doc = Document(path)
        file = path.name

        topic = file.upper().replace(".DOCX", "")
        if topic == "DEUTSCHE LITERATUR MONOGRAPHIEN":
            topic_normalised = "de-lit-monographien"
        elif topic == "DEUTSCHE LITERATUR TEXTE":
            topic_normalised = "de-lit-texte"
        elif topic == "ERSTAUSGABEN A - G":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben1"
        elif topic == "ERSTAUSGABEN H - M":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben2"
        elif topic == "ERSTAUSGABEN N - Z":
            topic = "erstausgaben"
            topic_normalised = "erstausgaben3"
        else:
            topic_lower = topic.lower()
            if "-" in topic_lower:
                topic_normalised = topic_lower.split("-")[0]
            elif "," in topic_lower:
                topic_normalised = topic_lower.split(",")[0]
            else:
                topic_normalised = topic_lower.split()[0]  # Split on spaces, take first word

            topic_normalised = unicodedata.normalize("NFC", topic_normalised)

            topic_normalised = topic_normalised.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')

        count = 0

        for table in doc.tables:
            for row in table.rows:
                if len(row.cells[0].text) >= 2:

                    text = row.cells[0].text
                    if re.search(r"^AUS! ", text):
                        continue

                    count += 1
                    text_normalised = unicodedata.normalize("NFC", text)
                    pattern = "['" + chr(8220) + chr(8221) + chr(8222) + "]"


                    replace_quotes = re.sub(pattern, chr(39), text_normalised)

                    find_price = re.search(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", replace_quotes)
                    if find_price:
                            find_price = find_price.group()
                            price_number = re.search(r'\d+', find_price)
                            find_price = int(price_number.group()) if price_number else None
                    else:
                        find_price = None
                    price_removed = re.sub(r"\(\s*€\s*\d+[.-]*\s*\)|\s*€\s*\d+[.-]*\s*", "", replace_quotes)
                    price_cleaned = re.sub(r"\ba`\s*", "", price_removed)

                    remove_exclamation = re.sub(r"^!\s*", "", price_cleaned)

                    text_clean = remove_exclamation.replace('\n', '. ')
                    text_clean = ' '.join(text_clean.split())

                    entries.append({
                        "text": text_clean,
                        "source": file,
                        "price": find_price,
                        "topic": topic,
                        "topic_normalised": topic_normalised,
                    })

        entries_file = topic_normalised + ".json"
        file_path = folder_prepped / entries_file

        with open(file_path, "w") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

        rprint(f"Entries were successfully saved to {entries_file}")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        total_entries = len(entries)

        log_entry = {
            "timestamp": timestamp,
            "topic": topic,
            "entries_created": total_entries,
            }
            # normalise normalize("NFC")
        if not processing_log.exists():
            raise FileNotFoundError("process_log file missing!")
        else:
            with open(processing_log, "r") as f:
                process_report = json.load(f)
                process_report.append(log_entry)

            with open(processing_log, "w") as f:
                json.dump(process_report, f, ensure_ascii=False, indent=2)

        if topic_normalised in ["erstausgaben1", "erstausgaben2"]:
            continue
        elif topic_normalised == "erstausgaben3":
            # load json files, combine them into unified records, move on to batching
            path1 = folder_prepped / "erstausgaben1.json"
            path2 = folder_prepped / "erstausgaben2.json"
            with open(path1, "r") as f1:
                erstausgaben1 = json.load(f1)
            with open(path2, "r") as f2:
                erstausgaben2 = json.load(f2)
            ea_combined = erstausgaben1 + erstausgaben2 + entries
            entries = ea_combined
            total_entries = len(entries)
            pass

read_entries()
