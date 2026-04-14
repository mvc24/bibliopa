"""Fix update columns

Revision ID: f22b3439a0e0
Revises: 6d4a826e1f97
Create Date: 2026-04-07 11:27:53.366838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f22b3439a0e0'
down_revision: Union[str, Sequence[str], None] = '6d4a826e1f97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at_books
        BEFORE UPDATE ON books
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at_people
        BEFORE UPDATE ON people
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at_books2people
        BEFORE UPDATE ON books2people
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at_users
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at()
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_books ON books")
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_people ON people")
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_books2people ON books2people")
    op.execute("DROP TRIGGER IF EXISTS set_updated_at_users ON users")

    op.execute("DROP FUNCTION IF EXISTS set_updated_at")
