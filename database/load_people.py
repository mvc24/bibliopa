from rich import print, inspect
import sys
import uuid
import json
import unicodedata
from pathlib import Path
from datetime import datetime
from connection import get_db_connection


file_path = Path("database/in_progress/pass2_results/results_pass2_002.json")
