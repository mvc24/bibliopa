"""add book index on visibility

Revision ID: 0e353367b092
Revises: b3f7d2c1a890
Create Date: 2026-05-22 14:25:07.550725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e353367b092'
down_revision: Union[str, Sequence[str], None] = 'b3f7d2c1a890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX books_visible_idx
        ON books (book_id)
        WHERE is_removed = FALSE AND is_active <> 0
    """)

def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS books_visible_idx")
