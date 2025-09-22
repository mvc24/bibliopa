from pprint import pp
import sys
import uuid
import json
import unicodedata
from pathlib import Path
from datetime import datetime

from anthropic import NotFoundError
from connection import get_db_connection
from psycopg2 import sql
sys.path.append(str(Path(__file__).parent.parent))
from tables.topics import get_topic_id_by_name

# file = Path("data/parsed/batch_aegypten_20250911-2255.json")
file_path = Path("data/parsed")

def prepare_entries(filename):
    full_file_path = Path(file_path / filename)
    books_data = []
    collect_people = []
    prices_data = []
    books2volumes_data = []
    books_admin_data = []

    collect_people_file = Path("database/collect_people.json")
    corrupt_log_file = Path("data/logs/corrupt_entries_log.json")
    review_entries_file = Path("data/logs/review_entries_log.json")

    processing_done = False
    loading_done = False
    success = False
    error_message = None
    entry_count =  0
    people_logged = 0


    if not full_file_path.is_file():
        raise FileNotFoundError(f"{filename} doesn't exist!")

    try:
        with open(full_file_path, "r") as f:
            entries = json.load(f)

        corrupt_entries = []
        entries_for_review = []

        for entry in entries:
            # Check if entry has parsing errors - quarantine corrupt entries
            if "error" in entry:
                corrupt_entries.append({
                    "source_file": filename,
                    "custom_id": entry.get("custom_id", "unknown"),
                    "error": entry["error"],
                    "raw_response": entry.get("raw_response", "")
                })
                continue  # Skip processing this corrupt entry

            if entry["parsed_entry"]["administrative"]["needs_review"]:
                entries_for_review.append(entry)
                continue

            # Process clean entries only
            # generate unique ids
            book_id = str(uuid.uuid4())
            price_id = str(uuid.uuid4())

            # topic id
            for key, value in entry["parsed_entry"].items():
                if isinstance(value, str):
                    entry["parsed_entry"][key] = unicodedata.normalize("NFD", value)
            topic = entry["parsed_entry"]["topic"].strip("'")

            topic_id = get_topic_id_by_name(topic)

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
                    volume_id =  str(uuid.uuid4())
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
                "source_filename": filename,
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
                                "book_id": str(book_id),
                                "composite_id": entry["custom_id"],
                                "source_filename": filename,
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
                            people_logged += 1
                    else:
                        collect_people.append({
                            "book_id": str(book_id),
                            "composite_id": entry["custom_id"],
                            "source_filename": filename,
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
                        people_logged += 1

        # pp(collect_people)

        if not collect_people_file.exists():
            raise FileNotFoundError("People file missing!")
        else:
            with open(collect_people_file, "r") as f:
                collected_people = json.load(f)
                collected_people.extend(collect_people)

            with open(collect_people_file, "w") as f:
                json.dump(collected_people, f, ensure_ascii=False, indent=2)

        # Handle corrupt entries logging
        corrupt_count = len(corrupt_entries)
        if corrupt_count > 0:
            if not corrupt_log_file.exists():
                raise FileNotFoundError("Corrupt entries file missing!")
            else:
                with open(corrupt_log_file, "r") as f:
                    existing_corrupt_entries = json.load(f)
                    existing_corrupt_entries.extend(corrupt_entries)

                with open(corrupt_log_file, "w") as f:
                    json.dump(existing_corrupt_entries, f, ensure_ascii=False, indent=2)

        # Handle entries that need review
        review_count = len(entries_for_review)
        if review_count > 0:
            if not review_entries_file.exists():
                raise FileNotFoundError("Review entries file missing!")
            else:
                with open(review_entries_file, "r") as f:
                    existing_review_entries = json.load(f)
                    existing_review_entries.extend(entries_for_review)

                with open(review_entries_file, "w") as f:
                    json.dump(existing_review_entries, f, ensure_ascii=False, indent=2)


        success = True
        processing_done = True
        entry_count = len(entries) - corrupt_count - review_count  # Only count clean entries

    except FileNotFoundError:
        success = False
        error_message = f"File {filename} not found"
        # Data collections stay empty

    except json.JSONDecodeError:
        success = False
        error_message = f"Invalid JSON in {filename}"

    except Exception as e:
        success = False
        error_message = f"Unexpected error: {str(e)}"


    status = {
        "success": success,
        "error_message": error_message,
        "filename": filename,
        "processing_done": processing_done,
        "loading_done": loading_done,
        "entry_count": entry_count,
        "people_logged": people_logged,
        "corrupt_entries_found": len(corrupt_entries) if 'corrupt_entries' in locals() else 0,
        "review_entries_found": len(entries_for_review) if 'entries_for_review' in locals() else 0,
        "data": {
            "books": books_data,
            "prices": prices_data,
            "admin": books_admin_data,
            "books2volumes": books2volumes_data
        },
        "timestamp": str(datetime.now())
    }
    # pp(f"status success: {status["success"]}")
    # pp(f"status error_message: {status["error_message"]}")
    # pp(f"status filename: {status["filename"]}")
    # pp(f"status processing_done: {status["processing_done"]}")
    # pp(f"status loading_done: {status["loading_done"]}")
    # pp(f"status entry_count: {status["entry_count"]}")
    # pp(f"status people_logged: {status["people_logged"]}")

    return status

# prepared_entries = prepare_entries(filename)

def load_entries(prepared_entries):
    books_data = prepared_entries["data"]["books"]
    prices_data = prepared_entries["data"]["prices"]
    books2volumes_data = prepared_entries["data"]["books2volumes"]
    books_admin_data = prepared_entries["data"]["admin"]
    filename = prepared_entries["filename"]
    loading_done = False
    success = False
    error_message = None


    conn, cur = get_db_connection()

    if conn is None:
        error_message = print(f"Connection failed!")
        return error_message

    try:
        # books
        # SQL_BOOKS = "INSERT INTO x VALUES ();"
        insert_books = """
        INSERT INTO books (
            book_id,
            title,
            subtitle,
            publisher,
            place_of_publication,
            publication_year,
            edition,
            pages,
            isbn,
            format_original,
            format_expanded,
            condition,
            copies,
            illustrations,
            packaging,
            topic_id,
            is_translation,
            original_language,
            is_multivolume,
            series_title,
            total_volumes)
        VALUES (
            %(book_id)s,
            %(title)s,
            %(subtitle)s,
            %(publisher)s,
            %(place_of_publication)s,
            %(publication_year)s,
            %(edition)s,
            %(pages)s,
            %(isbn)s,
            %(format_original)s,
            %(format_expanded)s,
            %(condition)s,
            %(copies)s,
            %(illustrations)s,
            %(packaging)s,
            %(topic_id)s,
            %(is_translation)s,
            %(original_language)s,
            %(is_multivolume)s,
            %(series_title)s,
            %(total_volumes)s
        );
        """
        for record in books_data:
            cur.execute(insert_books, record)

        # volumes
        insert_volumes = """
        INSERT INTO books2volumes (
            volume_id,
            book_id,
            volume_number,
            volume_title,
            pages,
            notes
        )
        VALUES (
            %(volume_id)s,
            %(book_id)s,
            %(volume_number)s,
            %(volume_title)s,
            %(pages)s,
            %(notes)s
        );
        """
        for record in books2volumes_data:
            cur.execute(insert_volumes, record)

        # prices
        insert_prices = """
        INSERT INTO prices (
            price_id,
            book_id,
            amount,
            is_original
        )
        VALUES (
            %(price_id)s,
            %(book_id)s,
            %(amount)s,
            %(is_original)s
        );
        """
        for record in prices_data:
            cur.execute(insert_prices, record)

        # admin
        insert_admin = """
        INSERT INTO book_admin (
            book_id,
            source_filename,
            original_entry,
            parsing_confidence,
            needs_review,
            verification_notes,
            composite_id
        )
        VALUES (
            %(book_id)s,
            %(source_filename)s,
            %(original_entry)s,
            %(parsing_confidence)s,
            %(needs_review)s,
            %(verification_notes)s,
            %(composite_id)s
        );
        """
        for record in books_admin_data:
            cur.execute(insert_admin, record)

        conn.commit()
        success = True
        loading_done = True
        pp(f"Successfully loaded {filename} to database.")

    except Exception as e:
        conn.rollback()
        success = False
        error_message = pp(f"Unexpected error: {str(e)}")

    finally:
        cur.close()
        conn.close()

        loading_status = {
            "filename": prepared_entries["filename"],
            "loading_done": loading_done,
            "timestamp_loading": str(datetime.now())
        }
    return loading_status

# load_entries(prepare_entries(filename))
