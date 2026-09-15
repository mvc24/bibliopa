"""remove source column from prices

Revision ID: 6f93590b2596
Revises: f5f469aed30e
Create Date: 2025-09-21 20:51:33.099341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f93590b2596'
down_revision: Union[str, Sequence[str], None] = 'f5f469aed30e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE prices DROP COLUMN source")


def downgrade() -> None:
    op.execute("ALTER TABLE prices ADD COLUMN source")
