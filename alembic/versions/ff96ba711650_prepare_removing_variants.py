"""prepare removing variants

Revision ID: ff96ba711650
Revises: ccdcbb9a0631
Create Date: 2026-05-12 13:47:28.470399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff96ba711650'
down_revision: Union[str, Sequence[str], None] = 'ccdcbb9a0631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Prepare removing variants table"""
    op.execute("ALTER TABLE books2people DROP CONSTRAINT books2people_variant_id_fkey;")


def downgrade() -> None:
    """Downgrade schema."""
    pass
