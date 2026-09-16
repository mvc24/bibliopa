"""load books

Revision ID: a5ab158c3eb5
Revises: 382c5a14404f
Create Date: 2026-01-23 10:11:37.861486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

# revision identifiers, used by Alembic.
revision: str = 'a5ab158c3eb5'
down_revision: Union[str, Sequence[str], None] = '382c5a14404f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in January 2026. Now a no-op.

    It bulk-inserted the validated books. The code it imported is archived in
    pipeline/iteration-1/07_load/initial_load/prep_books.py. The revision id
    stays so the chain is intact and `alembic upgrade head` builds an empty
    schema.
    """
    pass


def downgrade() -> None:
    pass
