"""Update topic names

Revision ID: 75a6066945d6
Revises: 2f41dc3393f9
Create Date: 2026-01-28 20:01:57.275438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import json
from pathlib import Path

# revision identifiers, used by Alembic.
revision: str = '75a6066945d6'
down_revision: Union[str, Sequence[str], None] = '2f41dc3393f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    json_path = Path("topic_slugs.json")
    with open(json_path) as f:
        mappings = json.load(f)

    # Update each topic
    for mapping in mappings:
        op.execute(f"""
            UPDATE topics
            SET topic_name ='{mapping['topic_name']}', topic_normalised = '{mapping['topic_normalised']}'
            WHERE topic_id = {mapping['topic_id']}
        """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
