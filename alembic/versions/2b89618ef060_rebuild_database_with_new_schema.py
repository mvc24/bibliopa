"""rebuild_database_with_new_schema

Revision ID: 2b89618ef060
Revises: a4defab8c92a
Create Date: 2026-01-20 14:52:16.484409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# revision identifiers, used by Alembic.
revision: str = '2b89618ef060'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

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

    PEOPLE_SCHEMA = {
        "person_id": "SERIAL PRIMARY KEY",
        "unified_id": "TEXT UNIQUE",
        "family_name": "TEXT",
        "given_names": "TEXT",
        "name_prefix": "TEXT",
        "name_particles": "TEXT",
        "name_suffix": "TEXT",
        "single_name": "TEXT",
        "is_organisation": "BOOLEAN DEFAULT FALSE",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    TOPICS_SCHEMA = {
        "topic_id": "SERIAL PRIMARY KEY",
        "topic_name": "TEXT NOT NULL UNIQUE",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "topic_normalised": "VARCHAR(255)"
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

    USERS_SCHEMA = {
        "user_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "username": "TEXT NOT NULL UNIQUE",
        "email": "TEXT NOT NULL UNIQUE",
        "password_hash": "TEXT NOT NULL",
        "role": "TEXT NOT NULL DEFAULT 'viewer'",
        "is_active": "BOOLEAN DEFAULT TRUE",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    SESSIONS_SCHEMA = {
        "session_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "user_id": "UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE",
        "session_token": "TEXT NOT NULL UNIQUE",
        "expires_at": "TIMESTAMP NOT NULL",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    # Variants deleted

    # PEOPLE_VARIANTS_SCHEMA = {
    #     "variant_id": "serial PRIMARY KEY",
    #     "person_id": "integer NOT NULL REFERENCES people(person_id)",
    #     "unified_id": "text NOT NULL",
    #     "variant_string": "text NOT NULL",
    #     "variant_normalised": "text NOT NULL",
    #     "source": "text",
    #     "created_at": "timestamp DEFAULT CURRENT_TIMESTAMP"
    # }



    """Drop all existing tables and recreate with new schema."""

    # Drop all tables (CASCADE handles foreign key dependencies)
    op.execute("DROP TABLE IF EXISTS sessions CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    op.execute("DROP TABLE IF EXISTS book_admin CASCADE")
    op.execute("DROP TABLE IF EXISTS books2people CASCADE")
    op.execute("DROP TABLE IF EXISTS books2volumes CASCADE")
    op.execute("DROP TABLE IF EXISTS prices CASCADE")
    op.execute("DROP TABLE IF EXISTS people CASCADE")
    op.execute("DROP TABLE IF EXISTS books CASCADE")
    op.execute("DROP TABLE IF EXISTS topics CASCADE")

    # Create tables in order (respecting foreign key dependencies)

    # Topics first (no dependencies)
    create_topics = "CREATE TABLE topics ("
    create_topics += ", ".join([f"{col} {dtype}" for col, dtype in TOPICS_SCHEMA.items()])
    create_topics += ");"
    op.execute(create_topics)

    # Books (depends on topics)
    create_books = "CREATE TABLE books ("
    create_books += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS_SCHEMA.items()])
    create_books += ");"
    op.execute(create_books)

    # People (no dependencies)
    create_people = "CREATE TABLE people ("
    create_people += ", ".join([f"{col} {dtype}" for col, dtype in PEOPLE_SCHEMA.items()])
    create_people += ");"
    op.execute(create_people)

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

    # Books2people (depends on books and people)
    create_b2p = "CREATE TABLE books2people ("
    create_b2p += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS2PEOPLE_SCHEMA.items()])
    create_b2p += ");"
    op.execute(create_b2p)

    # Book_admin (depends on books)
    create_admin = "CREATE TABLE book_admin ("
    create_admin += ", ".join([f"{col} {dtype}" for col, dtype in BOOK_ADMIN_SCHEMA.items()])
    create_admin += ");"
    op.execute(create_admin)

    # Users (no dependencies)
    create_users = "CREATE TABLE users ("
    create_users += ", ".join([f"{col} {dtype}" for col, dtype in USERS_SCHEMA.items()])
    create_users += ");"
    op.execute(create_users)

    # Sessions (depends on users)
    create_sessions = "CREATE TABLE sessions ("
    create_sessions += ", ".join([f"{col} {dtype}" for col, dtype in SESSIONS_SCHEMA.items()])
    create_sessions += ");"
    op.execute(create_sessions)


def downgrade() -> None:
    """Not implemented - this is a complete rebuild."""
    pass
