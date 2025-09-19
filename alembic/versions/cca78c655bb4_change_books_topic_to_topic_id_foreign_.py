"""change_books_topic_to_topic_id_foreign_key

Revision ID: cca78c655bb4
Revises: a9c3a198a8c4
Create Date: 2025-09-19 14:05:28.024551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cca78c655bb4'
down_revision: Union[str, Sequence[str], None] = 'a9c3a198a8c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new topic_id column
    op.execute("ALTER TABLE books ADD COLUMN topic_id UUID REFERENCES topics(topic_id);")

    # Drop the old topic column
    op.execute("ALTER TABLE books DROP COLUMN topic;")

def downgrade() -> None:
    # Add back the old topic column
    op.execute("ALTER TABLE books ADD COLUMN topic TEXT;")

    # Drop the topic_id column (this will also drop the foreign key constraint)
    op.execute("ALTER TABLE books DROP COLUMN topic_id;")
