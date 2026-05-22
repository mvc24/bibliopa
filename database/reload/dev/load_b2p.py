from rich import print
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_connection

b2p_file = Path("data_reload/b2p_loading_file.json")

def load_b2p_to_db():
    with open(b2p_file, "r") as f:
       b2p = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
    INSERT INTO books2people (book_id, composite_id, person_id, unified_id, display_name, family_name, given_names, name_prefix, name_particles, name_suffix, single_name, sort_order, is_author, is_editor, is_contributor, is_translator)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    """
    rows = [
        (
            entry.get("book_id"),
            entry.get("composite_id"),
            entry.get("person_id"),
            entry.get("unified_id"),
            entry.get("display_name"),
            entry.get("family_name"),
            entry.get("given_names"),
            entry.get("name_prefix"),
            entry.get("name_particles"),
            entry.get("name_suffix"),
            entry.get("single_name"),
            entry.get("sort_order"),
            entry.get("is_author"),
            entry.get("is_editor"),
            entry.get("is_contributor"),
            entry.get("is_translator"),
        ) for entry in b2p]

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()

    print(f"Done: attempted {len(rows)} rows")
    conn.close()
if __name__ == "__main__":
    load_b2p_to_db()
