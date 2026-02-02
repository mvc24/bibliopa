"""add foreign key indexes

Revision ID: 6ef7244b42c7
Revises: 75a6066945d6
Create Date: 2026-02-02 17:49:57.621577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ef7244b42c7'
down_revision: Union[str, Sequence[str], None] = '75a6066945d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Foreign key indexes
    op.create_index('ix_books_topic_id', 'books', ['topic_id'])
    op.create_index('ix_books2people_book_id', 'books2people', ['book_id'])
    op.create_index('ix_books2people_person_id', 'books2people', ['person_id'])
    op.create_index('ix_prices_book_id', 'prices', ['book_id'])
    op.create_index('ix_books2volumes_book_id', 'books2volumes', ['book_id'])

    # Filter index
    op.create_index('ix_books_is_removed', 'books', ['is_removed'])


def downgrade() -> None:
    # Drop in reverse order
    op.drop_index('ix_books_is_removed', table_name='books')
    op.drop_index('ix_books2volumes_book_id', table_name='books2volumes')
    op.drop_index('ix_prices_book_id', table_name='prices')
    op.drop_index('ix_books2people_person_id', table_name='books2people')
    op.drop_index('ix_books2people_book_id', table_name='books2people')
    op.drop_index('ix_books_topic_id', table_name='books')
