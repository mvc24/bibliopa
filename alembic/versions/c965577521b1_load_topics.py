"""load topics

Revision ID: c965577521b1
Revises: 2b89618ef060
Create Date: 2026-01-22 16:53:29.076354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.load_topics import load_topics


# revision identifiers, used by Alembic.
revision: str = 'c965577521b1'
down_revision: Union[str, Sequence[str], None] = '2b89618ef060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    topics_table = sa.table('topics',
        sa.column('topic_id', sa.Integer),
        sa.column('topic_name', sa.String)
    )
    topics_data = load_topics()
    op.bulk_insert(topics_table, topics_data)


def downgrade() -> None:
    op.execute("DELETE FROM topics")
