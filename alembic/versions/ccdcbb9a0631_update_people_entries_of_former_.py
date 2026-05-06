"""Update people entries of former multiples

Revision ID: ccdcbb9a0631
Revises: 46891a539b3e
Create Date: 2026-05-06 19:51:47.651049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError


import json
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'ccdcbb9a0631'
down_revision: Union[str, Sequence[str], None] = '46891a539b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    json_path = Path("data/people/people_to_update.json")
    with open(json_path) as f:
        people = json.load(f)

    update_stmt = sa.text("""
        UPDATE people
        SET unified_id = :unified_id,
            family_name = :family_name,
            given_names = :given_names,
            name_particles = :name_particles,
            single_name = :single_name,
            is_organisation = :is_organisation
        WHERE person_id = :person_id
    """)

    connection = op.get_bind()
    collisions = []

    for person in people:
        try:
            with connection.begin_nested():
                connection.execute(update_stmt, {
                    'person_id': person['person_id'],
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
        collisions_path = Path("data/people/update_collisions.json")
        with open(collisions_path, "w") as f:
            json.dump(collisions, f, indent=2, ensure_ascii=False)
        print(f"\n{len(collisions)} collisions written to {collisions_path}")
    else:
        print("No collisions.")


def downgrade() -> None:
    """Downgrade schema."""
    pass
