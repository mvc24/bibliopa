from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
sys.path.append(str(Path(__file__).parent.parent))

from database.tables.books import get_all_book_ids

prepped4load_folder = Path("data/prepped4load")
admin_data4loading_file = Path("data/admin_data4loading.json")
prices_data4loading_file = Path("data/prices_data4loading.json")
b2v_data4loading_file = Path("data/b2v_data4loading.json")
b2p_data4loading_file = Path("data/b2p_data4loading.json")

def load_related_tables():
    book_ids = get_all_book_ids()
    id_dict = {composite_id: book_id for composite_id, book_id in book_ids}

    books_admin_data = []
    prices_data = []
    books2people_data = []
    books2volumes_data = []

    for file in prepped4load_folder.iterdir():

        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist!")

        with open(file, "r") as f:
            entries = json.load(f)

        for composite_id, entry in entries.items():
            book_id = id_dict.get(composite_id)
            books2people = entry["books2people"]
            books2volumes = entry["books2volumes"]

            entry["admin"][0]["book_id"] = book_id

            entry["prices"][0]["book_id"] = book_id


            for person in books2people:
                person["book_id"] = book_id

            for volume in books2volumes:
                volume["book_id"] = book_id

            books_admin_data.append(entry["admin"][0])
            prices_data.append(entry["prices"][0])
            books2volumes_data.extend(books2volumes)
            books2people_data.extend(books2people)

    with open(admin_data4loading_file, "w") as f:
        json.dump(books_admin_data, f, ensure_ascii=False, indent=2)

    with open(prices_data4loading_file, "w") as f:
        json.dump(prices_data, f, ensure_ascii=False, indent=2)

    with open(b2p_data4loading_file, "w") as f:
        json.dump(books2people_data, f, ensure_ascii=False, indent=2)
    with open(b2v_data4loading_file, "w") as f:
        json.dump(books2volumes_data, f, ensure_ascii=False, indent=2)

    return books2people_data, prices_data, books2volumes_data, books_admin_data

load_related_tables()
