"""add status field to books table

Revision ID: 50f3cb025763
Revises: c25dfe60be3b
Create Date: 2026-01-28 18:43:37.477195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50f3cb025763'
down_revision: Union[str, Sequence[str], None] = 'c25dfe60be3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute('ALTER TABLE books ADD COLUMN is_removed BOOLEAN DEFAULT FALSE')

def downgrade():
    op.execute('ALTER TABLE books DROP COLUMN is_removed')
