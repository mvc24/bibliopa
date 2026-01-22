from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
import unicodedata
from connection import get_db_connection
from psycopg2 import sql
sys.path.append(str(Path(__file__).parent.parent))

from database import load_topics
from database.load_topics import get_topics
from database.load_people import load_people
from scripts.text_matching import normalise_text


file_path = Path("data/validated")
review_entries_file = Path("data/logs/review_entries_log.json")


def prepare_entries(filename):
    topics = load_topics()
    topic_lookup = {normalise_text((topic["topic_name"])): topic["topic_id"] for topic in topics}

    full_file_path = Path(file_path / filename)
    books_data = []
    books2people_data = []
    prices_data = []
    books2volumes_data = []
    books_admin_data = []

    processing_done = False
    loading_done = False
    success = False
    error_message = None
    critical_error = False
    entry_count =  0

    if not full_file_path.is_file():
        critical_error = True
        raise FileNotFoundError(f"{filename} doesn't exist!")
    if not review_entries_file.exists():
        critical_error = True
        raise FileNotFoundError("Review entries file missing!")

    try:
        with open(full_file_path, "r") as f:
            entries = json.load(f)
        entries_for_review = []

        for composite_id, entry in entries.items():
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
            series_title = entry["books"]["series_title"]
            total_volumes = entry["books"]["total_volumes"]
            source_filename = entry["admin"]["source_filename"]
            original_entry = entry["admin"]["original_entry"]
            parsing_confidence = entry["admin"]["parsing_confidence"]
            verification_notes = entry["admin"]["verification_notes"]
            topic_changed = entry["admin"]["topic_changed"]
            price_changed = entry["admin"]["price_changed"]

            if needs_review:
                entries_for_review.append(entry)
                continue

            # books

            # get topic id
            topic_normalised = normalise_text(topic)
            topic_id = topic_lookup.get(topic_normalised)

            books_data.append({
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
            })



            # admin


            # books2people
            for person in books2people:
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




    except FileNotFoundError:
        success = False
        critical_error = True
        error_message = f"File {filename} not found"
        # Data collections stay empty

    except json.JSONDecodeError:
        success = False
        error_message = f"Invalid JSON in {filename}"

    except Exception as e:
        success = False
        critical_error = True
        error_message = f"Unexpected error: {str(e)}"


    return
