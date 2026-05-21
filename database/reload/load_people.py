from rich import print
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_connection

people_file = Path("data_reload/people/people_file.json")

def load_people_to_db():
    with open(people_file, "r") as f:
        people = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
        INSERT INTO people (unified_id, family_name, given_names, name_prefix, name_particles, name_suffix, single_name, is_organisation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (unified_id) DO NOTHING
    """
    rows = [
    (
        person.get("unified_id"),
        person.get("family_name"),
        person.get("given_names"),
        person.get("name_prefix"),
        person.get("name_particles"),
        person.get("name_suffix"),
        person.get("single_name"),
        person.get("is_organisation"),
    ) for person in people]

    attempted_ids = [row[0] for row in rows]

    with conn.cursor() as cur:
        cur.execute("SELECT unified_id FROM people WHERE unified_id = ANY(%s)", [attempted_ids])
        existing = {row[0] for row in cur.fetchall()}

    if existing:
        print(f"{len(existing)} conflicts found:")
        for uid in existing:
            print(f"  {uid}")

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()

    print(f"Done: attempted {len(rows)} rows")
    conn.close()

if __name__ == "__main__":
    load_people_to_db()
