"""add trigram indexes

Revision ID: da311bdcaadf
Revises: dd57c5529964
Create Date: 2026-05-30 13:16:51.411236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da311bdcaadf'
down_revision: Union[str, Sequence[str], None] = 'dd57c5529964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE INDEX books_publisher_trgm ON books USING gin (publisher gin_trgm_ops)")
    op.execute("CREATE INDEX books_place_trgm ON books USING gin (place_of_publication gin_trgm_ops)")
    op.execute("CREATE INDEX books_title_trgm ON books USING gin (title gin_trgm_ops)")
    op.execute("CREATE INDEX people_family_name_trgm ON people USING gin (family_name gin_trgm_ops)")
    op.execute("CREATE INDEX people_single_name_trgm ON people USING gin (single_name gin_trgm_ops)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS books_publisher_trgm")
    op.execute("DROP INDEX IF EXISTS books_place_trgm")
    op.execute("DROP INDEX IF EXISTS books_title_trgm")
    op.execute("DROP INDEX IF EXISTS people_family_name_trgm")
    op.execute("DROP INDEX IF EXISTS people_single_name_trgm")
