import json
import argparse
from pathlib import Path
from datetime import datetime
from parse_single_batch import submit_batch

def get_available_topics():
    """Auto-discover topics that have batch files ready for processing"""
    batch_dir = Path("data/batched")
    available_topics = []
    
    if not batch_dir.exists():
        print(f"Warning: Batch directory {batch_dir} does not exist")
        return available_topics
    
    # Scan subdirectories in data/batched/
    for topic_dir in batch_dir.iterdir():
        if topic_dir.is_dir():
            # Check if directory contains .json batch files
            json_files = list(topic_dir.glob("*.json"))
            if json_files:
                available_topics.append(topic_dir.name)
                print(f"Found {len(json_files)} batch files for topic: {topic_dir.name}")
    
    available_topics.sort()  # Keep consistent ordering
    return available_topics

def find_batch_files():
    """Find all batch files for available topics"""
    batch_dir = Path("data/batched")
    files = []
    available_topics = get_available_topics()
    
    for topic in available_topics:
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

def run_batch_processor(max_submit=15):
    print("Starting batch processor...")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    
    # Discover available topics
    print("\n=== AUTO-DISCOVERING AVAILABLE TOPICS ===")
    available_topics = get_available_topics()
    print(f"Available topics ready for processing: {len(available_topics)}")
    
    if not available_topics:
        print("No topics found with batch files. Run data_prep.py first to create batch files.")
        return

    # Find files and load progress
    batch_files = find_batch_files()
    log_data = load_log()

    print(f"\nTotal batch files ready for submission: {len(batch_files)}")

    # PHASE 1: Submit new batches (max 5 at a time)
    print("\n=== SUBMITTING NEW BATCHES ===")
    submitted_files = set(log_data["submitted"].keys())
    new_files = [f for f in batch_files if str(f) not in submitted_files]

    print(f"New files to submit: {len(new_files)}")

    submit_count = 0
    # max_submit is now passed as parameter

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

    # Status checking moved to separate check_status.py script

    # SUMMARY
    print(f"\n=== SUBMISSION SUMMARY ===")
    print(f"Files submitted this run: {submit_count}")
    print(f"Total submitted: {len(log_data['submitted'])}")
    print(f"Total failed submissions: {len(log_data['failed'])}")
    
    if submit_count > 0:
        print(f"\n✓ Use 'python api/check_status.py' to monitor batch progress.")

def main():
    parser = argparse.ArgumentParser(
        description='Submit batch files to Claude API for processing'
    )
    parser.add_argument(
        '--max-submit', 
        type=int, 
        default=15,
        help='Maximum number of batches to submit in this run (default: 15)'
    )
    parser.add_argument(
        '--list-topics',
        action='store_true',
        help='List available topics and exit (no submission)'
    )
    
    args = parser.parse_args()
    
    if args.list_topics:
        print("Available topics with batch files:")
        topics = get_available_topics()
        if not topics:
            print("No topics found with batch files.")
            return
        
        for topic in topics:
            batch_count = len(list(Path(f"data/batched/{topic}").glob("*.json")))
            print(f"  {topic}: {batch_count} batch files")
        return
    
    print(f"Batch Processor - Max submissions: {args.max_submit}")
    run_batch_processor(max_submit=args.max_submit)

if __name__ == "__main__":
    main()
