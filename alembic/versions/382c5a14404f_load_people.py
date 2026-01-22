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
from database.load_people import load_people


# revision identifiers, used by Alembic.
revision: str = '382c5a14404f'
down_revision: Union[str, Sequence[str], None] = 'c965577521b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    people_data, _ = load_people()

    people_table = sa.table('people',
        sa.column('person_id', sa.Integer),
        sa.column('unified_id', sa.Text),
        sa.column('family_name', sa.Text),
        sa.column('given_names', sa.Text),
        sa.column('name_particles', sa.Text),
        sa.column('single_name', sa.Text),
        sa.column('is_organisation', sa.Boolean)
)

    op.bulk_insert(people_table, people_data)

    op.execute("""
        SELECT setval('people_person_id_seq', (SELECT MAX(person_id) FROM people));
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM people")
