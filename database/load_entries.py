from pprint import pp
import sys
import uuid
import json
import unicodedata
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))
from tables.topics import get_topic_id_by_name

filename = Path("data/parsed/batch_aegypten_20250911-2255.json")


def prepare_entries(filename):
    books_data = []
    collect_people = []
    prices_data = []
    books2volumes_data = []
    books_admin_data = []

    collect_people_file = Path("database/collect_people.json")

    if not filename.exists():
        raise FileNotFoundError(f"{filename} doesn't exist!")

    with open(filename, "r") as f:
        entries = json.load(f)

        for entry in entries:
            # generate unique ids
            book_id = uuid.uuid4()
            price_id = uuid.uuid4()

            # topic id
            for key, value in entry["parsed_entry"].items():
                if isinstance(value, str):
                    entry["parsed_entry"][key] = unicodedata.normalize("NFD", value)
            topic = entry["parsed_entry"]["topic"].strip("'")

            topic_id = get_topic_id_by_name(topic)
            # pp(topic_id)

            # books
            books_data.append({
                "book_id": book_id,
                "title": entry["parsed_entry"]["title"],
                "subtitle": entry["parsed_entry"]["subtitle"],
                "publisher": entry["parsed_entry"]["publisher"],
                "place_of_publication": entry["parsed_entry"]["place_of_publication"],
                "publication_year": entry["parsed_entry"]["publication_year"],
                "edition": entry["parsed_entry"]["edition"],
                "pages": entry["parsed_entry"]["pages"],
                "format_original": entry["parsed_entry"]["format_original"],
                "format_expanded": entry["parsed_entry"]["format_expanded"],
                "condition": entry["parsed_entry"]["condition"],
                "copies": entry["parsed_entry"]["copies"],
                "illustrations": entry["parsed_entry"]["illustrations"],
                "packaging": entry["parsed_entry"]["packaging"],
                "isbn": entry["parsed_entry"]["isbn"],
                "is_translation": entry["parsed_entry"]["is_translation"],
                "original_language": entry["parsed_entry"]["original_language"],
                "is_multivolume": entry["parsed_entry"]["is_multivolume"],
                "series_title": entry["parsed_entry"]["series_title"],
                "total_volumes": entry["parsed_entry"]["total_volumes"],
                "topic_id": topic_id
            })
            # pp(books_data)

            # books2volumes
            if entry["parsed_entry"]["is_multivolume"] == True:

                for volume in entry["parsed_entry"]["volumes"]:
                    volume_id =  uuid.uuid4()
                    books2volumes_data.append({
                        "volume_id": volume_id,
                        "book_id": book_id,
                        "volume_number": volume["volume_number"],
                        "volume_title": volume["volume_title"],
                        "pages": volume["pages"],
                        "notes": volume["notes"]
                    })

            # prices
            if entry["parsed_entry"]["price"]:
                is_original = True
            else:
                is_original = False

            prices_data.append({
                "price_id": price_id,
                "book_id": book_id,
                "is_original": is_original,
                "amount": entry["parsed_entry"]["price"],
            })

            # admin data
            verification_notes = entry["parsed_entry"]["administrative"].get("verification_notes", "")
            books_admin_data.append({
                "book_id": book_id,
                "composite_id": entry["custom_id"],
                "source_filename": filename.name,
                "original_entry": entry["parsed_entry"]["administrative"]["original_entry"],
                "parsing_confidence": entry["parsed_entry"]["administrative"]["parsing_confidence"],
                "needs_review": entry["parsed_entry"]["administrative"]["needs_review"],
                "verification_notes": verification_notes
            })
            # pp(books_admin_data)

            # handle people
            find_people = [
                ("author", entry["parsed_entry"]["authors"], True),
                ("editor", entry["parsed_entry"]["editors"], True),
                ("contributor", entry["parsed_entry"]["contributors"], True),
                ("translator", entry["parsed_entry"]["translator"], False)
            ]

            for role, people, is_list in find_people:
                if people:
                    if is_list:
                        for sort_order, person in enumerate(people):
                            collect_people.append({
                                "book_id": book_id,
                                "composite_id": entry["custom_id"],
                                "source_filename": filename.name,
                                "display_name": person["display_name"],
                                "family_name": person["family_name"],
                                "given_names": person["given_names"],
                                "name_particles": person["name_particles"],
                                "single_name": person["single_name"],
                                "is_author": (role == "author"),
                                "is_editor": (role == "editor"),
                                "is_contributor": (role == "contributor"),
                                "is_translator": (role == "translator"),
                                "sort_order": sort_order
                            })
                    else:
                        collect_people.append({
                            "book_id": book_id,
                            "composite_id": entry["custom_id"],
                            "source_filename": filename.name,
                            "display_name": people["display_name"],
                            "family_name": people["family_name"],
                            "given_names": people["given_names"],
                            "name_particles": people["name_particles"],
                            "single_name": people["single_name"],
                            "is_author": (role == "author"),
                            "is_editor": (role == "editor"),
                            "is_contributor": (role == "contributor"),
                            "is_translator": (role == "translator"),
                            "sort_order": 0
                            })
            # pp(collect_people)
            if not collect_people_file.exists():
                raise FileNotFoundError("People file missing!")
            else:
                with open(collect_people_file, "r") as f:
                    collected_people = json.load(f)
                    collected_people.extend(collect_people)

                with open(collect_people_file, "w") as f:
                    json.dump(collected_people, f, ensure_ascii=False, indent=2)


    return books_data, prices_data, books_admin_data, books2volumes_data
    # people_data, books2people_data

prepared_entries = prepare_entries(filename)
