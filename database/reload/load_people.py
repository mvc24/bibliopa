from rich import print, inspect
import sys
import json
from pathlib import Path
from datetime import datetime
from database import get_db_connection

people_file = Path("data_reload/people/people_file.json")

def load_people_to_db():
    with open(people_file, "r") as f:
       people = json.load(f)


    pass
