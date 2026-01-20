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
from database.table_schemas import (
    TOPICS_SCHEMA,
    BOOKS_SCHEMA,
    PEOPLE_SCHEMA,
    PRICES_SCHEMA,
    BOOKS2VOLUMES_SCHEMA,
    BOOKS2PEOPLE_SCHEMA,
    BOOK_ADMIN_SCHEMA,
    USERS_SCHEMA,
    SESSIONS_SCHEMA
)

# revision identifiers, used by Alembic.
revision: str = '2b89618ef060'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
