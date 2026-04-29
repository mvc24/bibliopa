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
from database.table_schemas import (
    BOOKS_SCHEMA,
    PRICES_SCHEMA,
    BOOKS2VOLUMES_SCHEMA,
    BOOKS2PEOPLE_SCHEMA,
    BOOK_ADMIN_SCHEMA,
)

# revision identifiers, used by Alembic.
revision: str = '46891a539b3e'
down_revision: Union[str, Sequence[str], None] = '1df4c8d9464d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop tables with major changes"""

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
