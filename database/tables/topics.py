from os import error
from pprint import pp
import sys
import unicodedata
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from database.connection import get_db_connection

def get_topic_id_by_name(topic_name):
    conn, cur = get_db_connection()
    if conn is None:
        print(f"Connection failed!")
        return

    try:
        topic_name = unicodedata.normalize("NFD", topic_name.strip())
        SQL = "SELECT topic_id FROM topics WHERE UPPER(TRIM(topic_name)) = UPPER(%s);"
        cur.execute(SQL, (topic_name,))
        topic_id = cur.fetchone()
        if topic_id is None:
            print(f"{topic_name} not found!")
            return None
        # pp(topic_id)
        # pp(topic_id[0])
        return topic_id[0]

    except Exception as e:
        print(f"Something went wrong!")
        return

    finally:
        conn.close()

def get_all_topics():
    conn, cur = get_db_connection()
    if conn is None:
        print(f"Connection failed!")
        return

    try:
        SQL = "SELECT * FROM topics"
        cur.execute(SQL)
        topics = cur.fetchall()
        if topics is None:
            print(f"topics were not found!")
            return None
        # pp(topics)
        return topics
    except Exception as e:
        print(f"Something went wrong!")
        return

    finally:
        conn.close()

# get_all_topics()
