"""Drop and rebuild people and b2p

Revision ID: 090f6e6b5219
Revises: edae66936413
Create Date: 2026-05-14 12:32:38.581865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



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

PEOPLE_SCHEMA = {
    "person_id": "SERIAL PRIMARY KEY",
    "unified_id": "TEXT UNIQUE",
    "family_name": "TEXT",
    "name_prefix": "TEXT",
    "name_particles": "TEXT",
    "name_suffix": "TEXT",
    "single_name": "TEXT",
    "is_organisation": "BOOLEAN DEFAULT FALSE",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}



# revision identifiers, used by Alembic.
revision: str = '090f6e6b5219'
down_revision: Union[str, Sequence[str], None] = 'edae66936413'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("DROP TABLE IF EXISTS books2people CASCADE")
    op.execute("DROP TABLE IF EXISTS people CASCADE")

    # create people first
    create_people = "CREATE TABLE people("
    create_people += ", ".join([f"{col} {dtype}" for col, dtype in PEOPLE_SCHEMA.items()])
    create_people += ");"
    op.execute(create_people)

    # Books2people (depends on books and people)
    create_b2p = "CREATE TABLE books2people ("
    create_b2p += ", ".join([f"{col} {dtype}" for col, dtype in BOOKS2PEOPLE_SCHEMA.items()])
    create_b2p += ");"
    op.execute(create_b2p)

    op.execute("""
        CREATE TRIGGER set_updated_at_people
        BEFORE UPDATE ON people
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
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_people ON people")
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_books2people ON books2people")
