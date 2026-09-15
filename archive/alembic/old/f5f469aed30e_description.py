"""remove batch_id

Revision ID: f5f469aed30e
Revises: b09e8410b966
Create Date: 2025-09-21 20:45:53.165620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5f469aed30e'
down_revision: Union[str, Sequence[str], None] = 'b09e8410b966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE book_admin DROP COLUMN batch_id")


def downgrade() -> None:
    op.execute("ALTER TABLE book_admin ADD COLUMN batch_id")
