"""load people

Revision ID: 382c5a14404f
Revises: c965577521b1
Create Date: 2026-01-22 16:57:27.533749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))


# revision identifiers, used by Alembic.
revision: str = '382c5a14404f'
down_revision: Union[str, Sequence[str], None] = 'c965577521b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in January 2026. Now a no-op.

    It bulk-inserted the validated people records and reset the id sequence.
    The code it imported is archived in
    pipeline/iteration-1/07_load/initial_load/load_people.py. The revision id
    stays so the chain is intact and `alembic upgrade head` builds an empty
    schema.
    """
    pass


def downgrade() -> None:
    pass
