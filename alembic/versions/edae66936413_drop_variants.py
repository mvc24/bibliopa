"""Drop variants

Revision ID: edae66936413
Revises: 1bb136f99df1
Create Date: 2026-05-14 11:24:06.895600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edae66936413'
down_revision: Union[str, Sequence[str], None] = '1bb136f99df1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('DROP TABLE people_variants')


def downgrade() -> None:
    """Downgrade schema."""
    pass
