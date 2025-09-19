from pprint import pp
import uuid
import json
from pathlib import Path
from datetime import datetime

filename = Path("data/parsed/batch_aegypten_20250911-2255.json")


def prepare_entries(filename):
    books_data = []
    people_data = []
    prices_data = []
    books2people_data = []
    books2volumes_data = []
    books_admin_data = []


    if not filename.exists():
        raise FileNotFoundError(f"{filename} doesn't exist!")

    with open(filename, "r") as f:
        entries = json.load(f)

        for entry in entries:
            # topics

            # books
            books_data.append({
                "book_id": uuid.uuid4(),
                "title": entry["parsed_entry"]["title"],
                "subtitle": entry["parsed_entry"]["subtitle"],
                "publisher":
                "place_of_publication":
                "publication_year":
                "edition":
                "pages":
                "format_original":
                "format_expanded":
                "condition":
                "copies":
                "illustrations":
                "packaging":
                "isbn":

            })


    return books_data, people_data, prices_data, books2people_data, books2volumes_data, books_admin_data

prepared_entries = prepare_entries(filename)
