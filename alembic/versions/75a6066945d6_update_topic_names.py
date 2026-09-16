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
    """Data migration, run once in January 2026. Now a no-op.

    It corrected topic names and slugs from topic_slugs.json, which is not
    in the repo. The revision id stays so the chain is intact.
    """
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
