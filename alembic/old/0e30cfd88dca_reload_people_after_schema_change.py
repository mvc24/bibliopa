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
    results_folder = Path("data/api_people/clean_results")

    insert_stmt = sa.text("""
        INSERT INTO people (unified_id, family_name, given_names, name_prefix, name_particles, name_suffix, single_name, is_organisation)
        VALUES (:unified_id, :family_name, :given_names, :name_prefix, :name_particles, :name_suffix, :single_name, :is_organisation)
    """)

    connection = op.get_bind()
    collisions = []

    files = sorted(results_folder.glob("*.json"))
    total_files = len(files)

    for file_idx, file in enumerate(files, start=1):
        print(f"[{file_idx}/{total_files}] Starting {file.name}...")

        with open(file, "r") as f:
            people = json.load(f)

        for person in people:
            try:
                with connection.begin_nested():
                    connection.execute(insert_stmt, {
                        'unified_id': person['unified_id'],
                        'family_name': person.get('family_name'),
                        'given_names': person.get('given_names'),
                        'name_prefix': person.get('name_prefix'),
                        'name_particles': person.get('name_particles'),
                        'name_suffix': person.get('name_suffix'),
                        'single_name': person.get('single_name'),
                        'is_organisation': person.get('is_organisation', False),
                    })
            except IntegrityError as e:
                collisions.append({
                    'person': person,
                    'error': str(e.orig).strip(),
                })
                print(f"  Skipped {person.get('unified_id', '?')}: collision")

        print(f"[{file_idx}/{total_files}] Finished {file.name} ({len(people)} entries)")

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
