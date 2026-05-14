"""reload people after schema change

Revision ID: 0e30cfd88dca
Revises: 090f6e6b5219
Create Date: 2026-05-14 13:24:06.174856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
import json
from pathlib import Path

# revision identifiers, used by Alembic.
revision: str = '0e30cfd88dca'
down_revision: Union[str, Sequence[str], None] = '090f6e6b5219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    json_path = Path("data/people/people_clean.json")
    with open(json_path, "r") as f:
        people = json.load(f)

    insert_stmt = sa.text("""
        INSERT INTO people (unified_id, family_name, given_names, name_prefix, name_particles, name_suffix, single_name, is_organisation)
        VALUES (:unified_id, :family_name, :given_names, :name_prefix, :name_particles, :name_suffix, :single_name, :is_organisation)
    """)

    connection = op.get_bind()
    collisions = []

    for person in people:
        try:
            with connection.begin_nested():
                connection.execute(insert_stmt, {
                    'unified_id': person['unified_id'],
                    'family_name': person['family_name'],
                    'given_names': person['given_names'],
                    'name_prefix': person['name_prefix'],
                    'name_particles': person['name_particles'],
                    'name_suffix': person['name_suffix'],
                    'single_name': person['single_name'],
                    'is_organisation': person['is_organisation'],
                })
        except IntegrityError as e:
            collisions.append({
                'person': person,
                'error': str(e.orig).strip(),
            })
            print(f"Skipped person_id {person['person_id']} ({person['unified_id']}): collision")
    if collisions:
        collisions_path = Path("data/people/insert_collisions.json")
        with open(collisions_path, "w") as f:
            json.dump(collisions, f, indent=2, ensure_ascii=False)
        print(f"\n{len(collisions)} collisions written to {collisions_path}")
    else:
        print("No collisions.")

def downgrade() -> None:
    """Downgrade schema."""
    pass
