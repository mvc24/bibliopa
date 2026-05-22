from rich import print as rprint
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_connection

admin_file = Path("data_reload/admin_data.json")
prices_file = Path("data_reload/prices_data.json")
volumes_file = Path("data_reload/volumes_data.json")


def load_book_admin():
    with open(admin_file, "r") as f:
        entries = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
    INSERT INTO book_admin (book_id, composite_id, original_entry, corrected_by_api, missing_person, multiple_editions, api_concerned, problematic_multi_volume, verification_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (book_id) DO NOTHING
    """
    rows = [
        (
            entry.get("book_id"),
            entry.get("composite_id"),
            entry.get("original_entry"),
            entry.get("corrected_by_api"),
            entry.get("missing_person"),
            entry.get("multiple_editions"),
            entry.get("api_concerned"),
            entry.get("problematic_multi_volume"),
            entry.get("verification_notes"),
        )
        for entry in entries
    ]

    attempted_ids = [row[0] for row in rows]

    with conn.cursor() as cur:
        cur.execute("SELECT book_id FROM book_admin WHERE book_id = ANY(%s)", [attempted_ids])
        existing = {row[0] for row in cur.fetchall()}

    if existing:
        print(f"{len(existing)} conflicts found:")
        for uid in existing:
            print(f"  {uid}")

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()

    rprint(f"found conflicts: {len(existing)}")
    print(f"Done: attempted {len(rows)} rows")
    conn.close()


def load_prices():
    with open(prices_file, "r") as f:
        entries = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
    INSERT INTO prices (book_id, amount, imported_price)
        VALUES (%s, %s, %s)
    """
    rows = [
        (
            entry.get("book_id"),
            entry.get("amount"),
            entry.get("imported_price"),
        )
        for entry in entries
    ]

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()

    print(f"Done: attempted {len(rows)} rows")
    conn.close()


def load_volumes():
    with open(volumes_file, "r") as f:
        entries = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
    INSERT INTO books2volumes (book_id, volume_number, volume_title, pages, notes)
        VALUES (%s, %s, %s, %s, %s)
    """
    rows = [
        (
            entry.get("book_id"),
            entry.get("volume_number"),
            entry.get("volume_title"),
            entry.get("pages"),
            entry.get("notes"),
        )
        for entry in entries
    ]

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()

    print(f"Done: attempted {len(rows)} rows")
    conn.close()


if __name__ == "__main__":
    load_book_admin()
    load_prices()
    load_volumes()
