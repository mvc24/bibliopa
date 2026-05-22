"""Update schema for new data

Revision ID: 46891a539b3e
Revises: 1df4c8d9464d
Create Date: 2026-04-29 16:02:01.458638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# revision identifiers, used by Alembic.
revision: str = '46891a539b3e'
down_revision: Union[str, Sequence[str], None] = '1df4c8d9464d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop tables with major changes"""

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

    BOOKS2VOLUMES_SCHEMA = {
        "volume_id": "SERIAL PRIMARY KEY",
        "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
        "volume_number": "INTEGER",
        "volume_title": "TEXT",
        "pages": "INTEGER",
        "notes": "TEXT"
    }

    BOOKS2PEOPLE_SCHEMA = {
        "b2p_id": "SERIAL PRIMARY KEY",
        "book_id": "INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE",
        "composite_id": "TEXT NOT NULL",
        "person_id": "INTEGER NOT NULL REFERENCES people(person_id) ON DELETE CASCADE",
        "unified_id": "TEXT NOT NULL",
        "display_name": "TEXT",
        "family_name": "TEXT",
        "given_names": "TEXT",
        "name_prefix": "TEXT",
        "name_particles": "TEXT",
        "name_suffix": "TEXT",
        "single_name": "TEXT",
        "sort_order": "INTEGER",
        "is_author": "BOOLEAN DEFAULT FALSE",
        "is_editor": "BOOLEAN DEFAULT FALSE",
        "is_contributor": "BOOLEAN DEFAULT FALSE",
        "is_translator": "BOOLEAN DEFAULT FALSE",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
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

    op.execute("DROP TABLE IF EXISTS books2people CASCADE")
    op.execute("DROP TABLE IF EXISTS books2volumes CASCADE")
    op.execute("DROP TABLE IF EXISTS book_admin CASCADE")
    op.execute("DROP TABLE IF EXISTS prices CASCADE")
    op.execute("DROP TABLE IF EXISTS books CASCADE")

    # Add trigger function for updates
    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$
    """)

    # Books (depends on topics)
    create_books = "CREATE TABLE books ("
    create_books += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS_SCHEMA.items()])
    create_books += ");"
    op.execute(create_books)

    # Prices (depends on books)
    create_prices = "CREATE TABLE prices ("
    create_prices += ", ".join([f"{col} {dtype}" for col, dtype in PRICES_SCHEMA.items()])
    create_prices += ");"
    op.execute(create_prices)

    # Books2volumes (depends on books)
    create_volumes = "CREATE TABLE books2volumes ("
    create_volumes += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS2VOLUMES_SCHEMA.items()])
    create_volumes += ");"
    op.execute(create_volumes)

    # Book_admin (depends on books)
    create_admin = "CREATE TABLE book_admin ("
    create_admin += ", ".join([f"{col} {dtype}" for col, dtype in BOOK_ADMIN_SCHEMA.items()])
    create_admin += ");"
    op.execute(create_admin)

    # Books2people (depends on books and people)
    create_b2p = "CREATE TABLE books2people ("
    create_b2p += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS2PEOPLE_SCHEMA.items()])
    create_b2p += ");"
    op.execute(create_b2p)

    op.execute("""
        CREATE TRIGGER set_updated_at_books
        BEFORE UPDATE ON books
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at_books2people
        BEFORE UPDATE ON books2people
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_books ON books")
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_books2people ON books2people")
