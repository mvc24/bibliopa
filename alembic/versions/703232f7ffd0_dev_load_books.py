"""dev_load_books

Revision ID: 703232f7ffd0
Revises: 0e30cfd88dca
Create Date: 2026-05-19 15:49:48.843976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, DataError

import json
import sys
from rich import print as rprint
from pathlib import Path

from database import connection


# revision identifiers, used by Alembic.
revision: str = '703232f7ffd0'
down_revision: Union[str, Sequence[str], None] = '0e30cfd88dca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Schemas hardcoded to make sure nothing breaks if I change things at a later point
BOOKS_SCHEMA = {
    "book_id": "SERIAL PRIMARY KEY",
    "composite_id": "TEXT UNIQUE",
    "is_active": "INTEGER",
    "is_removed": "BOOLEAN DEFAULT FALSE",
    "title": "TEXT NOT NULL",
    "subtitle": "TEXT",
    "publisher": "TEXT",
    "place_of_publication": "TEXT",
    "publication_year": "INTEGER",
    "edition": "TEXT",
    "pages": "INTEGER",
    "format_original": "TEXT",
    "format_expanded": "TEXT",
    "condition": "TEXT",
    "copies": "INTEGER",
    "illustrations": "TEXT",
    "packaging": "TEXT",
    "topic_id": "INTEGER REFERENCES topics(topic_id)",
    "is_translation": "BOOLEAN DEFAULT FALSE",
    "original_language": "TEXT",
    "is_multivolume": "BOOLEAN DEFAULT FALSE",
    "series_title": "TEXT",
    "total_volumes": "INTEGER",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

PRICES_SCHEMA = {
    "price_id": "SERIAL PRIMARY KEY",
    "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
    "amount": "INTEGER",
    "imported_price": "BOOLEAN NOT NULL DEFAULT FALSE",
    "source": "TEXT",
    "date_added": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

BOOK_ADMIN_SCHEMA = {
    "book_id": "INTEGER PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE",
    "composite_id": "TEXT REFERENCES books(composite_id) ON DELETE CASCADE",
    "original_entry": "TEXT NOT NULL",
    "corrected_by_api": "BOOLEAN DEFAULT FALSE",
    "missing_person": "BOOLEAN DEFAULT FALSE",
    "multiple_editions": "BOOLEAN DEFAULT FALSE",
    "api_concerned": "BOOLEAN DEFAULT FALSE",
    "problematic_multi_volume": "BOOLEAN DEFAULT FALSE",
    "verification_notes": "TEXT",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

BOOKS2VOLUMES_SCHEMA = {
    "volume_id": "SERIAL PRIMARY KEY",
    "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
    "volume_number": "INTEGER",
    "volume_title": "TEXT",
    "pages": "INTEGER",
    "notes": "TEXT"
}


loading_log_file = Path("data_reload/logs/book_loading_log.json")
books_folder = Path("data_reload/books/loading_batches")

books_insert = sa.text("""
INSERT INTO books (composite_id, is_active, is_removed, title, subtitle, publisher, place_of_publication, publication_year, edition, pages, format_original, format_expanded, condition, copies, illustrations, packaging, topic_id, is_translation, original_language, is_multivolume, series_title, total_volumes)
VALUES (:composite_id, :is_active, :is_removed, :title, :subtitle, :publisher, :place_of_publication, :publication_year, :edition, :pages, :format_original, :format_expanded, :condition, :copies, :illustrations, :packaging, :topic_id, :is_translation, :original_language, :is_multivolume, :series_title, :total_volumes)
RETURNING book_id
""")

prices_insert = sa.text("""
    INSERT INTO prices (book_id, amount, imported_price, source)
    VALUES (:book_id, :amount, :imported_price, :source)
""")

book_admin_insert = sa.text("""
    INSERT INTO book_admin (book_id, composite_id, original_entry, corrected_by_api, missing_person, multiple_editions, api_concerned, problematic_multi_volume, verification_notes)
    VALUES (:book_id, :composite_id, :original_entry, :corrected_by_api, :missing_person, :multiple_editions, :api_concerned, :problematic_multi_volume, :verification_notes)
""")

books2volumes_insert = sa.text("""
    INSERT INTO books2volumes (book_id, volume_number, volume_title, pages, notes)
    VALUES (:book_id, :volume_number, :volume_title, :pages, :notes)
""")

def to_int(val):
    """Normalize integer-coercible fields: convert empty strings to None."""
    if val == "":
        return None
    return val


def upgrade() -> None:
    """Upgrade schema."""

    connection = op.get_bind()

    if loading_log_file.exists():
        with open(loading_log_file, "r") as f:
            loading_log = json.load(f)
    else:
        loading_log = {}
    loading_log.setdefault("finished", [])
    loading_log.setdefault("errors", [])
    finished_batches = set(loading_log["finished"])

    files = sorted(books_folder.glob("*.json"))
    total_files = len(files)

    for file_idx, file in enumerate(files, start=1):
        filename = file.name
        rprint(f"[{file_idx}/{total_files}] Starting {filename}...")
        if filename in finished_batches:
            continue

        with open(file, "r") as f:
           books = json.load(f)

        for book_idx, (composite_id, book) in enumerate(books.items(), start=1):
            book_data = book[0]["books_data"]
            try:
                with connection.begin_nested():
                    result = connection.execute(books_insert, {
                        'composite_id': composite_id,
                        'is_active': to_int(book_data.get('is_active')),
                        'is_removed': book_data.get('is_removed', False),
                        'title': book_data.get('title'),
                        'subtitle': book_data.get('subtitle'),
                        'publisher': book_data.get('publisher'),
                        'place_of_publication': book_data.get('place_of_publication'),
                        'publication_year': to_int(book_data.get('publication_year')),
                        'edition': book_data.get('edition'),
                        'pages': to_int(book_data.get('pages')),
                        'format_original': book_data.get('format_original'),
                        'format_expanded': book_data.get('format_expanded'),
                        'condition': book_data.get('condition'),
                        'copies': to_int(book_data.get('copies')),
                        'illustrations': book_data.get('illustrations'),
                        'packaging': book_data.get('packaging'),
                        'topic_id': to_int(book_data.get('topic_id')),
                        'is_translation': book_data.get('is_translation'),
                        'original_language': book_data.get('original_language'),
                        'is_multivolume': book_data.get('is_multivolume'),
                        'series_title': book_data.get('series_title'),
                        'total_volumes': to_int(book_data.get('total_volumes')),
                    })
                    book_id = result.scalar()

                    price_data = book[0].get("price_data") or {}
                    if price_data:
                        connection.execute(prices_insert, {
                            'book_id': book_id,
                            'amount': to_int(price_data.get('amount')),
                            'imported_price': price_data.get('imported_price', True),
                            'source': price_data.get('source'),
                        })

                    admin_data = book[0].get("admin_data", {})
                    connection.execute(book_admin_insert, {
                        'book_id': book_id,
                        'composite_id': composite_id,
                        'original_entry': admin_data.get('original_entry'),
                        'corrected_by_api': admin_data.get('corrected_by_api', False),
                        'missing_person': admin_data.get('missing_person', False),
                        'multiple_editions': admin_data.get('multiple_editions', False),
                        'api_concerned': admin_data.get('api_concerned', False),
                        'problematic_multi_volume': admin_data.get('problematic_multi_volume', False),
                        'verification_notes': admin_data.get('verification_notes'),
                    })

                    volumes = (book[0].get("volumes_data") or {}).get("volumes") or []
                    for volume in volumes:
                        connection.execute(books2volumes_insert, {
                            'book_id': book_id,
                            'volume_number': to_int(volume.get('volume_number')),
                            'volume_title': volume.get('volume_title'),
                            'pages': to_int(volume.get('pages')),
                            'notes': volume.get('notes'),
                        })

            except (IntegrityError, DataError) as e:
                error_entry = {
                    'file': filename,
                    'composite_id': composite_id,
                    'error': str(e.orig).strip(),
                }
                loading_log["errors"].append(error_entry)
                with open(loading_log_file, "w") as f:
                    json.dump(loading_log, f, indent=2, ensure_ascii=False)
            if book_idx % 10 == 0:
                print("·", end="", flush=True)
        print()
        rprint(f"[{file_idx}/{total_files}] Finished {filename} ({len(books)} entries)")
        finished_batches.add(filename)
        loading_log["finished"].append(filename)
        with open(loading_log_file, "w") as f:
            json.dump(loading_log, f, indent=2, ensure_ascii=False)





def downgrade() -> None:
    """Downgrade schema."""
    pass
