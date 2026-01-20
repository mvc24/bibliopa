"""remove uuid generation

Revision ID: 8537dc93f793
Revises: cca78c655bb4
Create Date: 2025-09-19 16:20:22.727315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8537dc93f793'
down_revision: Union[str, Sequence[str], None] = 'cca78c655bb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # books
    op.execute("ALTER TABLE books ALTER COLUMN book_id DROP DEFAULT;")

    # people
    op.execute("ALTER TABLE people ALTER COLUMN person_id DROP DEFAULT;")

    # prices
    op.execute("ALTER TABLE prices ALTER COLUMN price_id DROP DEFAULT;")

    # books2volumes
    op.execute("ALTER TABLE books2volumes ALTER COLUMN volume_id DROP DEFAULT;")


def downgrade() -> None:
    """Downgrade schema."""
    pass
