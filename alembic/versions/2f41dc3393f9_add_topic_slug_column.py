"""add topic slug column

Revision ID: 2f41dc3393f9
Revises: 50f3cb025763
Create Date: 2026-01-28 19:19:28.697605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f41dc3393f9'
down_revision: Union[str, Sequence[str], None] = '50f3cb025763'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# migration file
import json
from pathlib import Path

def upgrade():
    # Add column
    op.execute('ALTER TABLE topics ADD COLUMN topic_normalised VARCHAR(255)')

    # Load mappings
    json_path = Path("topic_slugs.json")
    with open(json_path) as f:
        mappings = json.load(f)

    # Update each topic
    for mapping in mappings:
        op.execute(f"""
            UPDATE topics
            SET topic_normalised = '{mapping['topic_normalised']}'
            WHERE topic_id = {mapping['topic_id']}
        """)

def downgrade():
    op.execute('ALTER TABLE topics DROP COLUMN topic_normalised')
