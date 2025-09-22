"""remove constraint from prices

Revision ID: 8eba37ed6eb4
Revises: 6f93590b2596
Create Date: 2025-09-22 22:16:56.844533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eba37ed6eb4'
down_revision: Union[str, Sequence[str], None] = '6f93590b2596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE prices ALTER COLUMN amount DROP NOT NULL;")


def downgrade() -> None:
    """Downgrade schema."""
    pass
