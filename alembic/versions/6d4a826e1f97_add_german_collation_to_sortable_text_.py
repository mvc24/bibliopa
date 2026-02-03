"""Add German collation to sortable text columns

Revision ID: 6d4a826e1f97
Revises: 6ef7244b42c7
Create Date: 2026-02-03 20:19:35.248229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d4a826e1f97'
down_revision: Union[str, Sequence[str], None] = '6ef7244b42c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 op.execute("""
        ALTER TABLE people
        ALTER COLUMN family_name
        TYPE VARCHAR COLLATE "de-x-icu"
    """)

op.execute("""
    ALTER TABLE people
    ALTER COLUMN single_name
    TYPE VARCHAR COLLATE "de-x-icu"
""")

# Set German collation on topics table
op.execute("""
    ALTER TABLE topics
    ALTER COLUMN topic_name
    TYPE VARCHAR COLLATE "de-x-icu"
""")

# Set German collation on books table
op.execute("""
    ALTER TABLE books
    ALTER COLUMN title
    TYPE VARCHAR COLLATE "de-x-icu"
""")


def downgrade() -> None:
 op.execute("""
        ALTER TABLE people
        ALTER COLUMN family_name
        TYPE VARCHAR
    """)

op.execute("""
    ALTER TABLE people
    ALTER COLUMN single_name
    TYPE VARCHAR
""")

op.execute("""
    ALTER TABLE topics
    ALTER COLUMN topic_name
    TYPE VARCHAR
""")

op.execute("""
    ALTER TABLE books
    ALTER COLUMN title
    TYPE VARCHAR
""")
