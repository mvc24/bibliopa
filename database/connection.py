from pprint import pp
from psycopg import sql
from pathlib import Path
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg.connect(f"dbname={os.getenv("DB_NAME")} user={os.getenv("DB_USER")} password={os.getenv("DB_PW")} host={os.getenv("DB_HOST")} port={os.getenv("DB_PORT")} sslmode=require")
        return conn

    except:
        # print("Connection failed!")
        return None
