from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
sys.path.append(str(Path(__file__).parent.parent))

from database import load_topics
from database.load_topics import load_topics
from database.load_people import load_people
from scripts.text_matching import normalise_text

folder_validated = Path("data/validated")
review_entries_file = Path("data/logs/review_entries_log.json")
prepped4load_folder = Path("data/prepped4load")

review_entries_file = Path("data/logs/review_entries_log.json")
book_data_file = Path("data/book_data4loading.json")

def prepapre_books4loading():
    topics = load_topics()
    topic_lookup = {normalise_text((topic["topic_name"])): topic["topic_id"] for topic in topics}
    people_dict = load_people()[1]

    entries_for_review = []

    books_data_dict = {}

    for file in folder_validated.iterdir():


        prepped4loading_data = {}

        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist!")

        with open(file, "r") as f:
            entries = json.load(f)

        for composite_id, entry in entries.items():
            books2people_data = []
            prices_data = []
            books2volumes_data = []
            books_admin_data = []

            books2people = entry["books2people"]
            needs_review = entry["admin"]["needs_review"]
            title = entry["books"]["title"]
            subtitle = entry["books"]["subtitle"]
            publisher = entry["books"]["publisher"]
            place_of_publication = entry["books"]["place_of_publication"]
            publication_year = entry["books"]["publication_year"]
            edition = entry["books"]["edition"]
            pages = entry["books"]["pages"]
            isbn = entry["books"]["isbn"]
            format_original = entry["books"]["format_original"]
            format_expanded = entry["books"]["format_expanded"]
            condition = entry["books"]["condition"]
            copies = entry["books"]["copies"]
            illustrations = entry["books"]["illustrations"]
            packaging = entry["books"]["packaging"]
            topic = entry["books"]["topic"]
            is_translation = entry["books"]["is_translation"]
            original_language = entry["books"]["original_language"]
            is_multivolume = entry["books"]["is_multivolume"]
            volumes = entry["books"]["volumes"]
            series_title = entry["books"]["series_title"]
            total_volumes = entry["books"]["total_volumes"]
            source_filename = entry["admin"]["source_filename"]
            original_entry = entry["admin"]["original_entry"]
            parsing_confidence = entry["admin"]["parsing_confidence"]
            verification_notes = entry["admin"].get("verification_notes", "")
            topic_changed = entry["admin"]["topic_changed"]
            price_changed = entry["admin"]["price_changed"]
            amount = entry["books"]["price"]

            if not title:
                entries_for_review.append(entry)
                continue

            if needs_review:
                entries_for_review.append(entry)
                continue

            # books

            # get topic id
            topic_normalised = normalise_text(topic)
            topic_id = topic_lookup.get(topic_normalised)

            books_data_dict[composite_id] = {
                "composite_id": composite_id,
                "title": title,
                "subtitle": subtitle,
                "publisher": publisher,
                "place_of_publication": place_of_publication,
                "publication_year": publication_year,
                "edition": edition,
                "pages": pages,
                "isbn": isbn,
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
            }

            # admin

            books_admin_data.append({
                "book_id": None,
                "composite_id": composite_id,
                "source_filename": source_filename,
                "original_entry": original_entry,
                "parsing_confidence": parsing_confidence,
                "needs_review": needs_review,
                "verification_notes": verification_notes,
                "topic_changed": topic_changed,
                "price_changed": price_changed
            })

            # books2volumes
            if is_multivolume:
                for volume in volumes:
                    volume_number = volume["volume_number"]
                    volume_title = volume["volume_title"]
                    pages = volume["pages"]
                    notes = volume["notes"]
                    books2volumes_data.append({
                        "book_id": None,
                        "composite_id": composite_id,
                        "volume_number": volume_number,
                        "volume_title": volume_title,
                        "pages": pages,
                        "notes": notes,
                    })

            # books2people
            for person in books2people:
                unified_id = person["unified_id"]
                display_name = person["display_name"]
                family_name = person["family_name"]
                given_names = person["given_names"]
                name_particles = person["name_particles"]
                single_name = person["single_name"]
                sort_order = person["sort_order"]
                is_author = person["is_author"]
                is_editor = person["is_editor"]
                is_contributor = person["is_contributor"]
                is_translator = person["is_translator"]

                person_id = people_dict.get(unified_id)

                books2people_data.append({
                    "book_id": None,
                    "composite_id": composite_id,
                    "person_id": person_id,
                    "unified_id": unified_id,
                    "display_name": display_name,
                    "family_name": family_name,
                    "given_names": given_names,
                    "name_particles": name_particles,
                    "single_name": single_name,
                    "sort_order": sort_order,
                    "is_author": is_author,
                    "is_editor": is_editor,
                    "is_contributor": is_contributor,
                    "is_translator": is_translator,
                })

            # prices
            imported_price = False
            if price_changed == 1:
                imported_price = True
            prices_data.append({
                "book_id": None,
                "composite_id": composite_id,
                "amount": amount,
                "imported_price": imported_price
            })

            prepped4loading_data[composite_id] = {
                "books2people": books2people_data,
                "books2volumes": books2volumes_data,
                "admin": books_admin_data,
                "prices": prices_data
            }

        prepped_files_path = prepped4load_folder / file.name

        with open(prepped_files_path, "w") as f:
            json.dump(prepped4loading_data, f, ensure_ascii=False, indent=2)

        review_count = len(entries_for_review)
        if review_count > 0:
            with open(review_entries_file, "r") as f:
                existing_review_entries = json.load(f)
                existing_review_entries.extend(entries_for_review)

        rprint(f"Successfully saved {len(entries)} entries to {file.name}")
    books_data = list(books_data_dict.values())

    with open(book_data_file, "w") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)

    return books_data

prepapre_books4loading()
