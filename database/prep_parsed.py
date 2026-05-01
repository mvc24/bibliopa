from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
sys.path.append(str(Path(__file__).parent.parent))

from scripts.text_matching import normalise_text

folder_parsed = Path("data/parsed")
folder_prepped = Path("data/prepped")

topics_file = Path("data/from db/topics.json")
# people_var_file = Path("data/from_db/people_variants.json")
people_extracted_file = Path("database/people_extracted.json")

prep_log_file = Path("data/logs/prep_log.json")

def prep_parsed_data():

    people_dict = {}
    prep_log = {
        "critical": {},
        "report": {}
    }
    critical_count = 0


    with open(topics_file, "r") as f:
        topics = json.load(f)

    topics_lookup = {topic["topic_normalised"]: topic for topic in topics}
    # print(topics_lookup)


    for file in folder_parsed.iterdir():
        parsed_data = {}
        entry_count = 0
        people_count = 0

        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist!")


        parts = file.stem.split("_")
        topic = parts[1]
        # print(topic)

        with open(file, "r") as f:
            entries = json.load(f)
        # print(entries[:3])
        # break

        for entry in entries:
            try:
                entry_count += 1


                composite_id = entry["custom_id"]
                price = entry.get("price", None)
                parsed = entry["parsed_entry"]

                title = parsed["title"]
                subtitle = parsed["subtitle"]
                publisher = parsed["publisher"]
                place_of_publication = parsed["place_of_publication"]
                publication_year = parsed["publication_year"]
                edition = parsed["edition"]
                pages = parsed["pages"]

                format_original = parsed["format_original"]
                format_expanded = parsed["format_expanded"]
                condition = parsed["condition"]
                copies = parsed.get("copies", "")
                illustrations = parsed["illustrations"]
                packaging = parsed["packaging"]
                is_translation = parsed["is_translation"]
                original_language = parsed["original_language"]
                is_multivolume = parsed["is_multivolume"]
                volumes = parsed["volumes"]
                series_title = parsed["series_title"]
                total_volumes = parsed["total_volumes"]
                original_entry_pipes = parsed["administrative"]["original_entry"]
                is_reference = parsed["administrative"]["is_reference"]
                corrected_by_api = parsed["administrative"]["corrected_by_api"]
                missing_person = parsed["administrative"]["missing_person"]
                multiple_editions = parsed["administrative"]["multiple_editions"]
                api_concerned = parsed["administrative"]["api_concerned"]
                problematic_multi_volume = parsed["administrative"]["problematic_multi_volume"]
                verification_notes = parsed["administrative"].get("verification_notes", "")


                if is_reference == True:
                    continue

                # Get topic_id, log errors
                if topic in topics_lookup:
                    topic_id = topics_lookup[topic]["topic_id"]

                else:
                    if composite_id not in prep_log["critical"]:
                        prep_log["critical"][composite_id] = []
                    prep_log["critical"][composite_id].append("topic not found")
                    critical_count += 1


                # set is_active
                is_active = 1

                if api_concerned or problematic_multi_volume:
                    is_active = 0
                elif corrected_by_api or missing_person or multiple_editions or verification_notes:
                    is_active = 2

                # imported price
                if price:
                    imported_price = True
                else:
                    imported_price = False

                # format original entry
                original_entry = (
                    original_entry_pipes
                    .replace(" || ", "\n")
                    .replace("<<", "„")
                    .replace(">>", "“")
)

                # book data
                parsed_data[composite_id] = [
                    {
                        "books_data": {
                            "composite_id": composite_id,
                            "is_active": is_active,
                            "title": title,
                            "subtitle": subtitle,
                            "publisher": publisher,
                            "place_of_publication": place_of_publication,
                            "publication_year": publication_year,
                            "edition": edition,
                            "pages": pages,
                            "format_original": format_original,
                            "format_expanded": format_expanded,
                            "condition": condition,
                            "copies": copies,
                            "illustrations": illustrations,
                            "packaging": packaging,
                            "topic_id": topic_id,
                            "is_translation": is_translation,
                            "original_language": original_language,
                            "is_multivolume": is_multivolume,
                            "series_title": series_title,
                            "total_volumes": total_volumes
                        },

                        "admin_data": {
                            "composite_id": composite_id,
                            "original_entry": original_entry,
                            "corrected_by_api": corrected_by_api,
                            "missing_person": missing_person,
                            "multiple_editions": multiple_editions,
                            "api_concerned": api_concerned,
                            "problematic_multi_volume": problematic_multi_volume,
                            "verification_notes": verification_notes,
                        },

                        "price_data": {
                            "amount": price,
                            "imported_price": imported_price
                        },

                        "volumes_data": {
                            "volumes": volumes
                        }
                    }
                ]

                # prep people

                # if name_normalised not in people_dict:
                #     people_dict[name_normalised] = []

                # people_dict[name_normalised].append({
                #     "display_name": display_name,
                #     "composite_id": composite_id,
                #     "sort_order": sort_order,
                #     "is_author": True,   # adjust per role
                #     ...
                # })
                # people
                authors = parsed.get("authors") or []
                editors = parsed.get("editors") or []
                contributors = parsed.get("contributors") or []
                translator = parsed["translator"]


                for sort_order, person in enumerate(authors, start=1):
                    display_name = person["display_name"]
                    name_normalised = normalise_text(display_name)

                    if name_normalised not in people_dict:
                        people_dict[name_normalised] = []

                    people_dict[name_normalised].append({
                        "display_name": display_name,
                        "composite_id": composite_id,
                        "sort_order": sort_order,
                        "is_author": True,
                        "is_editor": False,
                        "is_contributor": False,
                        "is_translator": False
                    })
                    people_count += 1

                for sort_order, person in enumerate(editors, start=1):
                    display_name = person["display_name"]
                    name_normalised = normalise_text(display_name)

                    if name_normalised not in people_dict:
                        people_dict[name_normalised] = []

                    people_dict[name_normalised].append({
                        "display_name": display_name,
                        "composite_id": composite_id,
                        "sort_order": sort_order,
                        "is_author": False,
                        "is_editor": True,
                        "is_contributor": False,
                        "is_translator": False
                    })
                    people_count += 1

                for sort_order, person in enumerate(contributors, start=1):
                    display_name = person["display_name"]
                    name_normalised = normalise_text(display_name)

                    if name_normalised not in people_dict:
                        people_dict[name_normalised] = []

                    people_dict[name_normalised].append({
                        "display_name": display_name,
                        "composite_id": composite_id,
                        "sort_order": sort_order,
                        "is_author": False,
                        "is_editor": False,
                        "is_contributor": True,
                        "is_translator": False
                    })
                    people_count += 1

                if translator:
                    display_name = translator["display_name"]
                    name_normalised = normalise_text(display_name)

                    if name_normalised not in people_dict:
                        people_dict[name_normalised] = []

                    people_dict[name_normalised].append({
                        "display_name": display_name,
                        "composite_id": composite_id,
                        "sort_order": 1,
                        "is_author": False,
                        "is_editor": False,
                        "is_contributor": False,
                        "is_translator": True
                    })
                    people_count += 1


            except (KeyError, TypeError) as e:
                composite_id = entry.get("custom_id", "unknown")
                if composite_id not in prep_log["critical"]:
                    prep_log["critical"][composite_id] = []
                prep_log["critical"][composite_id].append(f"processing error: {e}")
                critical_count += 1
                continue


        # rprint(people_dict)
        # break

        if topic not in prep_log["report"]:
            prep_log["report"][topic] = {"entries": 0, "people": 0}
        prep_log["report"][topic]["entries"] += entry_count
        prep_log["report"][topic]["people"] += people_count

        output_file = folder_prepped / f"{topic}.json"

        if output_file.exists():
            with open(output_file, "r") as f:
                existing_data = json.load(f)
            existing_data.update(parsed_data)
            parsed_data = existing_data

        with open(output_file, "w") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)


        prep_log["totals"] = {
            "entries": sum(t["entries"] for t in prep_log["report"].values()),
            "unique_people": len(people_dict),
            "people_occurrences": sum(len(v) for v in people_dict.values())
        }

        with open(prep_log_file, "w") as f:
            json.dump(prep_log, f, ensure_ascii=False, indent=2)

        with open(people_extracted_file, "w") as f:
            json.dump(people_dict, f, ensure_ascii=False, indent=2)

prep_parsed_data()
