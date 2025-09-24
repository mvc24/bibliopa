"""remove constraint for volume number

Revision ID: 22351e7f42fb
Revises: 8eba37ed6eb4
Create Date: 2025-09-22 22:51:03.065722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22351e7f42fb'
down_revision: Union[str, Sequence[str], None] = '8eba37ed6eb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE books2volumes ALTER COLUMN volume_number DROP NOT NULL;")

def downgrade() -> None:
    """Downgrade schema."""
    pass
