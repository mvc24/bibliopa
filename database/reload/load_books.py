from rich import print as rprint
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_db_connection

books_file = Path("data_reload/books/books_data_file.json")

def load_books_to_db():
    with open(books_file, "r") as f:
       books = json.load(f)

    conn = get_db_connection()
    if conn is None:
        print("Connection failed")
        return

    insert_sql = """
    INSERT INTO books (composite_id, is_active, is_removed, title, subtitle, publisher, place_of_publication, publication_year, edition, pages, format_original, format_expanded, condition, copies, illustrations, packaging, topic_id, is_translation, original_language, is_multivolume, series_title, total_volumes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (composite_id) DO NOTHING
    """
    rows = [
        (
            book.get("composite_id"),
            book.get("is_active"),
            book.get("is_removed", False),
            book.get("title"),
            book.get("subtitle"),
            book.get("publisher"),
            book.get("place_of_publication"),
            book.get("publication_year") or None,
            book.get("edition"),
            book.get("pages") or None,
            book.get("format_original"),
            book.get("format_expanded"),
            book.get("condition"),
            book.get("copies") or None,
            book.get("illustrations"),
            book.get("packaging"),
            book.get("topic_id"),
            book.get("is_translation"),
            book.get("original_language"),
            book.get("is_multivolume"),
            book.get("series_title"),
            book.get("total_volumes") or None)
        for book in books]

    attempted_ids = [row[0] for row in rows]

    with conn.cursor() as cur:
        cur.execute("SELECT composite_id FROM books WHERE composite_id = ANY(%s)", [attempted_ids])
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

if __name__ == "__main__":
    load_books_to_db()
