"""create b2p index

Revision ID: dd57c5529964
Revises: 0e353367b092
Create Date: 2026-05-27 16:10:53.385360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd57c5529964'
down_revision: Union[str, Sequence[str], None] = '0e353367b092'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # books2people
    op.create_index('ix_books2people_book_id', 'books2people', ['book_id'])
    op.create_index('ix_books2people_is_author_person_id', 'books2people', ['is_author', 'person_id'])

    # prices
    op.create_index('ix_prices_book_id', 'prices', ['book_id'])
    op.execute("CREATE INDEX ix_prices_notnull_amount ON prices (book_id) WHERE amount IS NOT NULL")

    # books2volumes
    op.create_index('ix_books2volumes_book_id', 'books2volumes', ['book_id'])

    # topics
    op.create_index('ix_topics_topic_normalised', 'topics', ['topic_normalised'])

    # books
    op.create_index('ix_books_topic_id', 'books', ['topic_id'])
    op.create_index('ix_books_publication_year', 'books', ['publication_year'])

    # people: expression index for ORDER BY COALESCE(family_name, single_name)
    op.execute("CREATE INDEX ix_people_sort_name ON people (COALESCE(family_name, single_name), given_names)")


def downgrade() -> None:
    op.drop_index('ix_books2people_book_id', table_name='books2people')
    op.drop_index('ix_books2people_is_author_person_id', table_name='books2people')
    op.drop_index('ix_prices_book_id', table_name='prices')
    op.execute("DROP INDEX IF EXISTS ix_prices_notnull_amount")
    op.drop_index('ix_books2volumes_book_id', table_name='books2volumes')
    op.drop_index('ix_topics_topic_normalised', table_name='topics')
    op.drop_index('ix_books_topic_id', table_name='books')
    op.drop_index('ix_books_publication_year', table_name='books')
    op.execute("DROP INDEX IF EXISTS ix_people_sort_name")
