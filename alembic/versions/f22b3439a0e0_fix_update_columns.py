"""Fix update columns

Revision ID: f22b3439a0e0
Revises: 6d4a826e1f97
Create Date: 2026-04-07 11:27:53.366838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f22b3439a0e0'
down_revision: Union[str, Sequence[str], None] = '6d4a826e1f97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:


    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
