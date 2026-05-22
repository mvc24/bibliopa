"""Re-add German collation to sortable text columns

Revision ID: b3f7d2c1a890
Revises: 090f6e6b5219
Create Date: 2026-05-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f7d2c1a890'
down_revision: Union[str, Sequence[str], None] = '090f6e6b5219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE people
        ALTER COLUMN family_name
        TYPE TEXT COLLATE "de-x-icu"
    """)

    op.execute("""
        ALTER TABLE people
        ALTER COLUMN single_name
        TYPE TEXT COLLATE "de-x-icu"
    """)

    op.execute("""
        ALTER TABLE topics
        ALTER COLUMN topic_name
        TYPE TEXT COLLATE "de-x-icu"
    """)

    op.execute("""
        ALTER TABLE books
        ALTER COLUMN title
        TYPE TEXT COLLATE "de-x-icu"
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE people
        ALTER COLUMN family_name
        TYPE TEXT
    """)

    op.execute("""
        ALTER TABLE people
        ALTER COLUMN single_name
        TYPE TEXT
    """)

    op.execute("""
        ALTER TABLE topics
        ALTER COLUMN topic_name
        TYPE TEXT
    """)

    op.execute("""
        ALTER TABLE books
        ALTER COLUMN title
        TYPE TEXT
    """)
