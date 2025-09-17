"""Initial migration

Revision ID: a9c3a198a8c4
Revises:
Create Date: 2025-09-17 17:36:43.785755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9c3a198a8c4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline migration - tables already exist."""
    # Tables already exist, this migration just establishes the baseline
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
