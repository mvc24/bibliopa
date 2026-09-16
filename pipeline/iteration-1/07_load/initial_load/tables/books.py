import sys
import unicodedata
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.connection import get_db_connection

def get_all_books():
    conn, cur = get_db_connection()
    if conn is None:
        print(f"Connection failed!")
        return

    try:
        SQL = "SELECT * FROM books"
        cur.execute(SQL)
        books = cur.fetchall()
        if books is None:
            print(f"No books were found!")
            return None
        return books

    except Exception as e:
        print(f"Something went wrong!")
        return

    finally:
        conn.close()


def get_all_book_ids():
    conn, cur = get_db_connection()
    if conn is None:
        print(f"Connection failed!")
        return

    try:
        SQL = "SELECT composite_id, book_id FROM books"
        cur.execute(SQL)
        book_ids = cur.fetchall()
        if book_ids is None:
            print(f"No book_ids were were found!")
            return None
        return book_ids

    except Exception as e:
        print(f"Something went wrong!")
        return

    finally:
        conn.close()
