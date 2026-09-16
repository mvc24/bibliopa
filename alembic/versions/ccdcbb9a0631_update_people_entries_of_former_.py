"""Update people entries of former multiples

Revision ID: ccdcbb9a0631
Revises: 46891a539b3e
Create Date: 2026-05-06 19:51:47.651049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError


import json
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'ccdcbb9a0631'
down_revision: Union[str, Sequence[str], None] = '46891a539b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in April 2026 during the reload. Now a no-op.

    It updated people rows that had been split from multi-person strings,
    reading data/people/people_to_update.json, which is not in the repo. The
    people work of the reload is archived in pipeline/iteration-2/04_people/.
    The revision id stays so the chain is intact.
    """
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
