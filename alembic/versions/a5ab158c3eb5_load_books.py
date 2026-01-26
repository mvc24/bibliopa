"""load books

Revision ID: a5ab158c3eb5
Revises: 382c5a14404f
Create Date: 2026-01-23 10:11:37.861486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.prep_books import prepare_books4loading

# revision identifiers, used by Alembic.
revision: str = 'a5ab158c3eb5'
down_revision: Union[str, Sequence[str], None] = '382c5a14404f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    books_data = prepare_books4loading()

    books_table = sa.table("books",
        sa.column('composite_id', sa.Text),
        sa.column('title', sa.Text),
        sa.column('subtitle', sa.Text),
        sa.column('publisher', sa.Text),
        sa.column('place_of_publication', sa.Text),
        sa.column('publication_year', sa.Integer),
        sa.column('edition', sa.Text),
        sa.column('pages', sa.Integer),
        sa.column('isbn', sa.Text),
        sa.column('format_original', sa.Text),
        sa.column('format_expanded', sa.Text),
        sa.column('condition', sa.Text),
        sa.column('copies', sa.Integer),
        sa.column('illustrations', sa.Text),
        sa.column('packaging', sa.Text),
        sa.column('topic_id', sa.Integer),
        sa.column('is_translation', sa.Boolean),
        sa.column('original_language', sa.Text),
        sa.column('is_multivolume', sa.Boolean),
        sa.column('series_title', sa.Text),
        sa.column('total_volumes', sa.Integer)
    )

    op.bulk_insert(books_table, books_data)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER SEQUENCE books_book_id_seq RESTART WITH 1")
    op.execute("DELETE FROM books")
