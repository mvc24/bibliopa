"""change volume constraints

Revision ID: fe66ae4269ae
Revises: 22351e7f42fb
Create Date: 2025-09-24 15:27:39.237757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe66ae4269ae'
down_revision: Union[str, Sequence[str], None] = '22351e7f42fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE books2volumes DROP CONSTRAINT books2volumes_book_id_volume_number_key;")
    op.execute("ALTER TABLE books2volumes ADD COLUMN volume_index INTEGER;")
    op.execute("ALTER TABLE books2volumes ADD CONSTRAINT books2volumes_book_id_volume_index_key UNIQUE (book_id, volume_index);")

def downgrade() -> None:
    op.execute("ALTER TABLE books2volumes DROP COLUMN volume_index;")
    op.execute("ALTER TABLE books2volumes DROP CONSTRAINT books2volumes_book_id_volume_index_key;")
