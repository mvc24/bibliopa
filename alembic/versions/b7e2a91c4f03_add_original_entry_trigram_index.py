"""add original_entry trigram index

Revision ID: b7e2a91c4f03
Revises: da311bdcaadf
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e2a91c4f03'
down_revision: Union[str, Sequence[str], None] = 'da311bdcaadf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE INDEX book_admin_original_entry_trgm "
        "ON book_admin USING gin (original_entry gin_trgm_ops)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS book_admin_original_entry_trgm")
