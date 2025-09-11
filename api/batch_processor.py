import json
import time
from pathlib import Path
from datetime import datetime
from parse_single_batch import submit_batch, retrieve_batch_results

# Topics that have been prepared (xs + s groups)
PREPARED_TOPICS = [
    "symbolkunde",     # SYMBOLKUNDE
    "autographen",     # AUTOGRAPHEN
    "geschichte",      # GESCHICHTE ALLGEMEIN LÄNDER
    "maerchen",        # MÄRCHEN
    "suchliste",       # SUCHLISTE
    "zeitschriften",   # ZEITSCHRIFTEN
    "aegypten",        # ÄGYPTEN VORDERER ORIENT
    "buddhismus",      # BUDDHISMUS, HINDUISMUS
    "esoterik",        # ESOTERIK
    "islam",           # ISLAM
    "kinder",          # KINDER- UND JUGENDLITERATUR
    "monographien",    # MONOGRAPHIEN FREMDSPRACHIGER AUTOREN
    "mythologie",      # MYTHOLOGIE
    "renaissance",     # RENAISSANCE
    "sonstiges",       # SONSTIGES, BILDBÄNDE, KATALOGE ATLANTEN
    "zeitgeschichte"   # ZEITGESCHICHTE, REPORTAGEN
]

def find_batch_files():
    """Find batch files for prepared topics only"""
    batch_dir = Path("data/batched")
    files = []
    for topic in PREPARED_TOPICS:
        topic_files = list(batch_dir.glob(f"{topic}/*.json"))
        files.extend(topic_files)
    return files

def load_log():
    """Load existing progress log"""
    log_file = Path("data/logs/batch_progress.json")
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return {"submitted": {}, "completed": [], "failed": []}

def save_log(log_data):
    """Save progress log"""
    log_file = Path("data/logs/batch_progress.json")
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

def extract_topic_from_path(file_path):
    return file_path.parent.name

def run_batch_processor():
    print("Starting batch processor...")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")

    # Find files and load progress
    batch_files = find_batch_files()
    log_data = load_log()

    print(f"Found {len(batch_files)} batch files to process")

    # PHASE 1: Submit new batches (max 5 at a time)
    print("\n=== SUBMITTING NEW BATCHES ===")
    submitted_files = set(log_data["submitted"].keys())
    new_files = [f for f in batch_files if str(f) not in submitted_files]

    print(f"New files to submit: {len(new_files)}")

    submit_count = 0
    max_submit = 5  # Rate limit protection

    for file_path in new_files:
        if submit_count >= max_submit:
            print(f"Reached submission limit ({max_submit}). Will submit more in next run.")
            break

        try:
            print(f"Submitting: {file_path}")
            result = submit_batch(file_path)

            # Store submission info
            log_data["submitted"][str(file_path)] = {
                "batch_id": result["batch_id"],
                "topic": extract_topic_from_path(file_path),
                "submitted_at": timestamp,
                "entry_count": result["entry_count"]
            }

            submit_count += 1
            print(f"✓ Submitted: {result['batch_id']}")

            # Save progress after each submission
            save_log(log_data)

        except Exception as e:
            print(f"✗ Failed to submit {file_path}: {e}")
            log_data["failed"].append({
                "file_path": str(file_path),
                "error": str(e),
                "timestamp": timestamp
            })
            save_log(log_data)

    # PHASE 2: Check status of submitted batches
    print(f"\n=== CHECKING SUBMITTED BATCHES ===")
    completed_batch_ids = set(log_data["completed"])

    for file_path, submission_info in log_data["submitted"].items():
        batch_id = submission_info["batch_id"]

        if batch_id in completed_batch_ids:
            print(f"Already completed: {batch_id}")
            continue

        try:
            print(f"Checking: {batch_id} ({submission_info['topic']})")
            result = retrieve_batch_results(batch_id, submission_info["topic"])

            if result["status"] == "completed":
                print(f"✓ Completed: {result['output_file']} ({result['results_count']} results)")
                log_data["completed"].append(batch_id)
                save_log(log_data)

            elif result["status"] == "processing":
                print(f"⏳ Still processing: {batch_id}")

        except Exception as e:
            print(f"✗ Error checking {batch_id}: {e}")
            log_data["failed"].append({
                "batch_id": batch_id,
                "error": str(e),
                "timestamp": timestamp
            })
            save_log(log_data)

    # SUMMARY
    print(f"\n=== SUMMARY ===")
    print(f"Files submitted this run: {submit_count}")
    print(f"Total submitted: {len(log_data['submitted'])}")
    print(f"Total completed: {len(log_data['completed'])}")
    print(f"Total failed: {len(log_data['failed'])}")

    pending = len(log_data["submitted"]) - len(log_data["completed"])
    print(f"Still processing: {pending}")

    if pending > 0:
        print(f"\nRun again in 10-15 minutes to check for completed batches.")

if __name__ == "__main__":
    run_batch_processor()
