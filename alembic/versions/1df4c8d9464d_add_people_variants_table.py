"""add people variants table

Revision ID: 1df4c8d9464d
Revises: f22b3439a0e0
Create Date: 2026-04-24 16:55:57.752599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.table_schemas import (PEOPLE_VARIANTS_SCHEMA)

# revision identifiers, used by Alembic.
revision: str = '1df4c8d9464d'
down_revision: Union[str, Sequence[str], None] = 'f22b3439a0e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    create_variants = "CREATE TABLE people_variants("
    create_variants += ", ".join([f"{col} {dtype}" for col, dtype in PEOPLE_VARIANTS_SCHEMA.items()])
    create_variants += ");"
    op.execute(create_variants)
    op.execute("ALTER TABLE people_variants ADD CONSTRAINT uq_person_variant UNIQUE (person_id, variant_normalised);")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS people_variants")
