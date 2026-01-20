"""add unified_id to people table

Revision ID: a4defab8c92a
Revises: 035c5133ac4a
Create Date: 2026-01-20 12:24:27.949820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4defab8c92a'
down_revision: Union[str, Sequence[str], None] = '035c5133ac4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE people ALTER COLUMN person_id TYPE text")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
