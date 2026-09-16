"""load people from file

Revision ID: 1bb136f99df1
Revises: ff96ba711650
Create Date: 2026-05-12 13:53:20.325151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

import json
from pathlib import Path

# revision identifiers, used by Alembic.
revision: str = '1bb136f99df1'
down_revision: Union[str, Sequence[str], None] = 'ff96ba711650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in May 2026 during the reload. Now a no-op.

    It inserted new people rows from data/people/messy_shit/people_to_add.json,
    which is not in the repo. The people work of the reload is archived in
    pipeline/iteration-2/04_people/. The revision id stays so the chain is
    intact.
    """
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass
