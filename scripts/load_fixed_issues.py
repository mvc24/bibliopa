"""Load manually-fixed entries from data_reload/books/issues_fixed.json.

One-off loader for entries that were excluded from the main books migration
because of data issues that have since been corrected by hand.

Uses the same insert structure as alembic/versions/703232f7ffd0_dev_load_books.py
(books -> prices -> book_admin -> books2volumes per entry, all wrapped in a
savepoint so one bad row can fail without taking down the others).

Run from the project root:
    python scripts/load_fixed_issues.py
"""
import json
import sys
from pathlib import Path

# Make the project root importable so `from database.connection import ...` works
# regardless of where the script is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich import print as rprint

from database.connection import get_db_connection



FIXED_FILE = Path("data_reload/books/issues_fixed.json")


BOOKS_INSERT = """
    INSERT INTO books (composite_id, is_active, is_removed, title, subtitle, publisher, place_of_publication, publication_year, edition, pages, format_original, format_expanded, condition, copies, illustrations, packaging, topic_id, is_translation, original_language, is_multivolume, series_title, total_volumes)
    VALUES (%(composite_id)s, %(is_active)s, %(is_removed)s, %(title)s, %(subtitle)s, %(publisher)s, %(place_of_publication)s, %(publication_year)s, %(edition)s, %(pages)s, %(format_original)s, %(format_expanded)s, %(condition)s, %(copies)s, %(illustrations)s, %(packaging)s, %(topic_id)s, %(is_translation)s, %(original_language)s, %(is_multivolume)s, %(series_title)s, %(total_volumes)s)
    RETURNING book_id
"""

PRICES_INSERT = """
    INSERT INTO prices (book_id, amount, imported_price, source)
    VALUES (%(book_id)s, %(amount)s, %(imported_price)s, %(source)s)
"""

BOOK_ADMIN_INSERT = """
    INSERT INTO book_admin (book_id, composite_id, original_entry, corrected_by_api, missing_person, multiple_editions, api_concerned, problematic_multi_volume, verification_notes)
    VALUES (%(book_id)s, %(composite_id)s, %(original_entry)s, %(corrected_by_api)s, %(missing_person)s, %(multiple_editions)s, %(api_concerned)s, %(problematic_multi_volume)s, %(verification_notes)s)
"""

BOOKS2VOLUMES_INSERT = """
    INSERT INTO books2volumes (book_id, volume_number, volume_title, pages, notes)
    VALUES (%(book_id)s, %(volume_number)s, %(volume_title)s, %(pages)s, %(notes)s)
"""


def to_int(val):
    """Normalize integer-coercible fields: convert empty strings to None."""
    if val == "":
        return None
    return val


def main():
    with open(FIXED_FILE, "r") as f:
        entries = json.load(f)

    rprint(f"Loading {len(entries)} fixed entries from {FIXED_FILE}...")

    conn = get_db_connection()
    if conn is None:
        rprint("[red]Connection failed. Check .env settings.[/red]")
        return

    successes = []
    failures = []

    try:
        with conn.transaction():
            for composite_id, entry in entries.items():
                book_data = entry[0]["books_data"]
                try:
                    with conn.transaction():  # savepoint per entry
                        with conn.cursor() as cur:
                            cur.execute(BOOKS_INSERT, {
                                'composite_id': composite_id,
                                'is_active': to_int(book_data.get('is_active')),
                                'is_removed': book_data.get('is_removed', False),
                                'title': book_data.get('title'),
                                'subtitle': book_data.get('subtitle'),
                                'publisher': book_data.get('publisher'),
                                'place_of_publication': book_data.get('place_of_publication'),
                                'publication_year': to_int(book_data.get('publication_year')),
                                'edition': book_data.get('edition'),
                                'pages': to_int(book_data.get('pages')),
                                'format_original': book_data.get('format_original'),
                                'format_expanded': book_data.get('format_expanded'),
                                'condition': book_data.get('condition'),
                                'copies': to_int(book_data.get('copies')),
                                'illustrations': book_data.get('illustrations'),
                                'packaging': book_data.get('packaging'),
                                'topic_id': to_int(book_data.get('topic_id')),
                                'is_translation': book_data.get('is_translation'),
                                'original_language': book_data.get('original_language'),
                                'is_multivolume': book_data.get('is_multivolume'),
                                'series_title': book_data.get('series_title'),
                                'total_volumes': to_int(book_data.get('total_volumes')),
                            })
                            book_id = cur.fetchone()[0]

                            price_data = entry[0].get("price_data") or {}
                            if price_data:
                                cur.execute(PRICES_INSERT, {
                                    'book_id': book_id,
                                    'amount': to_int(price_data.get('amount')),
                                    'imported_price': price_data.get('imported_price', True),
                                    'source': price_data.get('source'),
                                })

                            admin_data = entry[0].get("admin_data") or {}
                            cur.execute(BOOK_ADMIN_INSERT, {
                                'book_id': book_id,
                                'composite_id': composite_id,
                                'original_entry': admin_data.get('original_entry'),
                                'corrected_by_api': admin_data.get('corrected_by_api', False),
                                'missing_person': admin_data.get('missing_person', False),
                                'multiple_editions': admin_data.get('multiple_editions', False),
                                'api_concerned': admin_data.get('api_concerned', False),
                                'problematic_multi_volume': admin_data.get('problematic_multi_volume', False),
                                'verification_notes': admin_data.get('verification_notes'),
                            })

                            volumes = (entry[0].get("volumes_data") or {}).get("volumes") or []
                            for volume in volumes:
                                cur.execute(BOOKS2VOLUMES_INSERT, {
                                    'book_id': book_id,
                                    'volume_number': to_int(volume.get('volume_number')),
                                    'volume_title': volume.get('volume_title'),
                                    'pages': to_int(volume.get('pages')),
                                    'notes': volume.get('notes'),
                                })

                    successes.append((composite_id, book_id))
                    rprint(f"[green]OK[/green] {composite_id} -> book_id {book_id}")

                except Exception as e:
                    failures.append((composite_id, str(e).strip()))
                    rprint(f"[red]FAIL[/red] {composite_id}: {str(e).strip()}")
    finally:
        conn.close()

    rprint(f"\n[bold]Done.[/bold] {len(successes)} loaded, {len(failures)} failed.")
    if failures:
        for composite_id, err in failures:
            rprint(f"  - {composite_id}: {err}")


if __name__ == "__main__":
    main()
