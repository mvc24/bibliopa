"""update_people_and_books2people_schema

Revision ID: 035c5133ac4a
Revises: fe66ae4269ae
Create Date: 2025-12-30 13:07:09.790713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '035c5133ac4a'
down_revision: Union[str, Sequence[str], None] = 'fe66ae4269ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE people ADD COLUMN is_organisation BOOLEAN DEFAULT FALSE")

    op.execute("ALTER TABLE books2people DROP CONSTRAINT books2people_role_check")

    op.execute("ALTER TABLE books2people DROP COLUMN role")

    op.execute("ALTER TABLE books2people ADD COLUMN display_name TEXT NOT NULL")
    op.execute("ALTER TABLE books2people ADD COLUMN family_name TEXT")
    op.execute("ALTER TABLE books2people ADD COLUMN given_names TEXT")
    op.execute("ALTER TABLE books2people ADD COLUMN name_particles TEXT")
    op.execute("ALTER TABLE books2people ADD COLUMN single_name TEXT")

    op.execute("ALTER TABLE books2people ADD COLUMN is_author BOOLEAN")
    op.execute("ALTER TABLE books2people ADD COLUMN is_editor BOOLEAN")
    op.execute("ALTER TABLE books2people ADD COLUMN is_contributor BOOLEAN")
    op.execute("ALTER TABLE books2people ADD COLUMN is_translator BOOLEAN")

def downgrade() -> None:
    """Downgrade schema."""
    pass
