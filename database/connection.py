from pprint import pp
import psycopg2
from psycopg2 import sql
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(f"dbname={os.getenv("DB_NAME")} user={os.getenv("DB_USER")} password={os.getenv("DB_PW")} host={os.getenv("DB_HOST")} port={os.getenv("DB_PORT")}")
        cur = conn.cursor()
        # print("connection created")
        return conn, cur
    except:
        # print("Connection failed!")
        return None, None
