"""dev_load_new_people

Revision ID: 6ed9a7f9583c
Revises: 703232f7ffd0
Create Date: 2026-05-20 13:18:52.107425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, DataError
import json
from pathlib import Path
from rich import print as rprint

from database import connection

# revision identifiers, used by Alembic.
revision: str = '6ed9a7f9583c'
down_revision: Union[str, Sequence[str], None] = '703232f7ffd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

people_batched_folder = Path("data_reload/people/people_batched")
people_loading_log_file = Path("data_reload/logs/people_loading_log.json")

insert_stmt = sa.text("""
        INSERT INTO people (unified_id, family_name, given_names, name_prefix, name_particles, name_suffix, single_name, is_organisation)
        VALUES (:unified_id, :family_name, :given_names, :name_prefix, :name_particles, :name_suffix, :single_name, :is_organisation)
    """)


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    if people_loading_log_file.exists():
        with open(people_loading_log_file, "r") as f:
            loading_log = json.load(f)
    else:
        loading_log = {}
    loading_log.setdefault("finished", [])
    loading_log.setdefault("errors", [])
    finished_batches = set(loading_log["finished"])

    files = sorted(people_batched_folder.glob("*.json"))
    total_files = len(files)

    for file_idx, file in enumerate(files, start=1):
        filename = file.name
        rprint(f"[{file_idx}/{total_files}] Starting {filename}...")
        if filename in finished_batches:
            continue

        with open(file, "r") as f:
           people = json.load(f)

        for person_idx, person in enumerate(people, start=1):
            unified_id = person["unified_id"]
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
            except (IntegrityError, DataError) as e:
                error_entry = {
                    'file': filename,
                    'unified_id': unified_id,
                    'error': str(e.orig).strip(),
                }
                loading_log["errors"].append(error_entry)
                with open(people_loading_log_file, "w") as f:
                    json.dump(loading_log, f, indent=2, ensure_ascii=False)
            if person_idx % 10 == 0:
                print("·", end="", flush=True)

        rprint(f"[{file_idx}/{total_files}] Finished {filename} ({len(people)} entries)")
        finished_batches.add(filename)
        loading_log["finished"].append(filename)
        with open(people_loading_log_file, "w") as f:
            json.dump(loading_log, f, ensure_ascii=False, indent=2)


def downgrade() -> None:
    """Downgrade schema."""
    pass
