from rich import print as rprint
from rich import inspect
import json
import sys
from datetime import datetime
from pathlib import Path
import json
sys.path.append(str(Path(__file__).parent.parent))

from database.tables.books import get_all_book_ids

prepped4load_folder = Path("data/prepped4load")
