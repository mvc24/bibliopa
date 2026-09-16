"""load related tables data

Revision ID: c25dfe60be3b
Revises: a5ab158c3eb5
Create Date: 2026-01-26 17:26:12.367602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))



# revision identifiers, used by Alembic.
revision: str = 'c25dfe60be3b'
down_revision: Union[str, Sequence[str], None] = 'a5ab158c3eb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in January 2026. Now a no-op.

    It bulk-inserted book_admin, prices, books2volumes and books2people after
    reading the assigned book ids back out of the books table. The code it
    imported is archived in
    pipeline/iteration-1/07_load/initial_load/prep_related_tables.py. The
    revision id stays so the chain is intact and `alembic upgrade head`
    builds an empty schema.
    """
    pass


def downgrade() -> None:
    pass
