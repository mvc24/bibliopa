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



# revision identifiers, used by Alembic.
revision: str = 'c965577521b1'
down_revision: Union[str, Sequence[str], None] = '2b89618ef060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Data migration, run once in January 2026. Now a no-op.

    It inserted the topics derived from the Word document names. The code it
    imported is archived in pipeline/iteration-1/07_load/initial_load/
    (load_topics.py, get_topics.py). The revision id stays so the chain is
    intact and `alembic upgrade head` builds an empty schema.
    """
    pass


def downgrade() -> None:
    pass
