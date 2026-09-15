"""load topics

Revision ID: b09e8410b966
Revises: 8537dc93f793
Create Date: 2025-09-19 17:49:46.946308

"""
from json import load
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.load_topics import load_topics


# revision identifiers, used by Alembic.
revision: str = 'b09e8410b966'
down_revision: Union[str, Sequence[str], None] = '8537dc93f793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    topics_table = sa.table('topics',
        sa.column('topic_id', sa.UUID),
        sa.column('topic_name', sa.String)
    )
    topics_data = load_topics()
    op.bulk_insert(topics_table, topics_data)


def downgrade() -> None:
    op.execute("DELETE FROM topics")
