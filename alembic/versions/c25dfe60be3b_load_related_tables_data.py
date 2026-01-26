"""load related tables data

Revision ID: c25dfe60be3b
Revises: a5ab158c3eb5
Create Date: 2026-01-26 17:26:12.367602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.prep_related_tables import prep_related_tables


# revision identifiers, used by Alembic.
revision: str = 'c25dfe60be3b'
down_revision: Union[str, Sequence[str], None] = 'a5ab158c3eb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Clear any partial data from previous failed runs
    op.execute("DELETE FROM books2volumes")
    op.execute("DELETE FROM books2people")
    op.execute("DELETE FROM prices")
    op.execute("DELETE FROM book_admin")

    admin_data, prices_data, b2p_data, b2v_data = prep_related_tables()

    admin_table = sa.table("book_admin",
        sa.column("book_id", sa.Integer),
        sa.column("composite_id", sa.Text),
        sa.column("original_entry", sa.Text),
        sa.column("parsing_confidence", sa.Text),
        sa.column("needs_review", sa.Boolean),
        sa.column("verification_notes", sa.Text),
        sa.column("topic_changed", sa.Boolean),
        sa.column("price_changed", sa.Boolean),
        sa.column("batch_id", sa.Text))

    prices_table = sa.table("prices",
        sa.column("book_id", sa.Integer),
        sa.column("amount", sa.Integer),
        sa.column("imported_price", sa.Boolean))

    books2people_table = sa.table("books2people",
        sa.column("book_id", sa.Integer),
        sa.column("composite_id", sa.Text),
        sa.column("person_id", sa.Integer),
        sa.column("unified_id", sa.Text),
        sa.column("display_name", sa.Text),
        sa.column("family_name", sa.Text),
        sa.column("given_names", sa.Text),
        sa.column("name_particles", sa.Text),
        sa.column("single_name", sa.Text),
        sa.column("sort_order", sa.Integer),
        sa.column("is_author", sa.Boolean),
        sa.column("is_editor", sa.Boolean),
        sa.column("is_contributor", sa.Boolean),
        sa.column("is_translator", sa.Boolean))

    books2volumes_table = sa.table("books2volumes",
        sa.column("book_id", sa.Integer),
        sa.column("volume_number", sa.Integer),
        sa.column("volume_title", sa.Text),
        sa.column("pages", sa.Integer),
        sa.column("notes", sa.Text))

    op.bulk_insert(admin_table, admin_data)
    op.bulk_insert(prices_table, prices_data)
    op.bulk_insert(books2volumes_table, b2v_data)
    batch_size = 1000
    for i in range(0, len(b2p_data), batch_size):
        batch = b2p_data[i:i + batch_size]
        op.bulk_insert(books2people_table, batch)
        print(f"Inserted books2people batch {i//batch_size + 1}/{(len(b2p_data) + batch_size - 1)//batch_size}")


def downgrade() -> None:
    """Downgrade schema."""
    # Restart sequences for tables with SERIAL primary keys
    op.execute("ALTER SEQUENCE books2volumes_volume_id_seq RESTART WITH 1")
    op.execute("ALTER SEQUENCE prices_price_id_seq RESTART WITH 1")

    # Delete data in reverse order of insertion
    op.execute("DELETE FROM books2volumes")
    op.execute("DELETE FROM books2people")
    op.execute("DELETE FROM prices")
    op.execute("DELETE FROM book_admin")
