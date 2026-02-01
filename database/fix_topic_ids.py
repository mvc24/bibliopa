from os import error
from pprint import pp
import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from database.connection import get_db_connection

mapping_file = Path("mapping.json")

def fix_topic_ids():
    conn = get_db_connection()  # returns only conn
    if conn is None:
        print(f"Connection failed!")
        return
    with conn.cursor() as cur:

        try:
            with open(mapping_file, "r") as f:
                mapping = json.load(f)

            for composite_id, topic_id in mapping.items():
                cur.execute(t"UPDATE books SET topic_id = {topic_id} WHERE composite_id = {composite_id}")
                print(f"Updated {cur.rowcount} rows")
                conn.commit()


        except Exception as e:
            print(f"Something went wrong!")
            return

        finally:
            conn.close()

fix_topic_ids()
