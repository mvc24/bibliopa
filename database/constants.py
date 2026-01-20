from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = PROJECT_ROOT / "database"

# Data subdirectories
PARSED_DIR = DATA_DIR / "parsed"
LOGS_DIR = DATA_DIR / "logs"
PEOPLE_DIR = DATA_DIR / "people"
MATCHED_DIR = DATA_DIR / "matched"
VALIDATED_DIR = DATA_DIR / "validated"

# Logs

VALIDATION_LOG = LOGS_DIR / "validation_failed_log.json"


PEOPLE_PREPPED_FILE = PEOPLE_DIR / "people_records_prepped.json"
BOOKS2PEOPLE_PREPPED_FILE = PEOPLE_DIR / "books2people_prepped.json"
