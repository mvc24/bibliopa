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

            for i, (composite_id, topic_id) in enumerate(mapping.items(), 1):
                cur.execute(t"UPDATE books SET topic_id = {topic_id}, updated_at = NOW() WHERE composite_id = {composite_id}")

                if i % 100 == 0:  # Print every 100 rows
                    print(f"Processed {i} rows so far...")

                conn.commit()

            print(f"Finished! Total rows processed: {i}")


        except Exception as e:
            print(f"Something went wrong!")
            return

        finally:
            conn.close()

fix_topic_ids()
