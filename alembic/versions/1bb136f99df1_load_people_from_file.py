"""load people from file

Revision ID: 1bb136f99df1
Revises: ff96ba711650
Create Date: 2026-05-12 13:53:20.325151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

import json
from pathlib import Path

# revision identifiers, used by Alembic.
revision: str = '1bb136f99df1'
down_revision: Union[str, Sequence[str], None] = 'ff96ba711650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    json_path = Path("data/people/messy_shit/people_to_add.json")
    with open(json_path, "r") as f:
       people = json.load(f)

    insert_stmt = sa.text("""
        INSERT INTO people (unified_id, family_name, given_names, name_particles, single_name, is_organisation)
        VALUES (:unified_id, :family_name, :given_names, :name_particles, :single_name, :is_organisation)
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
                    'name_particles': person['name_particles'],
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
