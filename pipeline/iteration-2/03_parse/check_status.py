import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import anthropic
from dotenv import load_dotenv

# Load environment variables and create API client
load_dotenv()
client = anthropic.Anthropic()


# ============================================================
# File and log helpers
# ============================================================

def load_log():
    """Load existing progress log."""
    log_file = Path("data/logs/batch_progress.json")
    if log_file.exists():
        with open(log_file, "r") as f:
            return json.load(f)
    return {"submitted": {}, "completed": [], "failed": []}


def save_log(log_data):
    """Save progress log."""
    log_file = Path("data/logs/batch_progress.json")
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def find_batch_files():
    """Find all batch files in data/raw/batched/<topic>/*.json."""
    batch_dir = Path("data/raw/batched")
    if not batch_dir.exists():
        return []

    files = []
    for topic_dir in batch_dir.iterdir():
        if topic_dir.is_dir():
            files.extend(topic_dir.glob("*.json"))
    return sorted(files)


def parsed_file_for(batch_file_path):
    """Return the expected parsed-output path for a given batch file."""
    stem = Path(batch_file_path).stem
    return Path(f"data/parsed/batch_{stem}.json")


# ============================================================
# Categorisation
# ============================================================

def categorise_batches(batch_files, log_data):
    """
    Bucket every batch file into one of three states:
      - parsed:        submitted AND output file exists in data/parsed/
      - in_queue:      submitted but no output file yet
      - not_submitted: file exists locally but no submission record

    Trusts the filesystem over the log: a batch is 'parsed & saved'
    only if its output file actually exists, regardless of what the
    'completed' array says.
    """
    submitted = log_data["submitted"]

    parsed = []         # list of (file_str, submission_info)
    in_queue = []       # list of (file_str, submission_info)
    not_submitted = []  # list of file_str

    for file_path in batch_files:
        file_str = str(file_path)
        if file_str in submitted:
            if parsed_file_for(file_path).exists():
                parsed.append((file_str, submitted[file_str]))
            else:
                in_queue.append((file_str, submitted[file_str]))
        else:
            not_submitted.append(file_str)

    return {
        "parsed": parsed,
        "in_queue": in_queue,
        "not_submitted": not_submitted,
        "total": len(batch_files),
    }


# ============================================================
# API retrieval
# ============================================================

def retrieve_batch(batch_id, original_file):
    """
    Check a batch's status; if ended, retrieve and save its results.
    Returns one of: 'completed', 'processing'.
    Saves results to data/parsed/batch_<filename>.json on success.

    Stays silent during normal operation — the caller decides what
    to print.
    """
    with open(original_file, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    lookup = {entry["composite_id"]: entry for entry in batch_data}

    batch_status = client.messages.batches.retrieve(batch_id)
    if batch_status.processing_status != "ended":
        return "processing"

    batch_results = client.messages.batches.results(batch_id)
    results_data = []

    for result in batch_results:
        if result.result and result.result.type == "succeeded":
            response_text = result.result.message.content[0].text

            if response_text.startswith("```json"):
                response_text = response_text.replace("```json\n", "").replace("\n```", "")

            try:
                parsed_json = json.loads(response_text)
                results_data.append({
                    "custom_id": result.custom_id,
                    "price": lookup.get(result.custom_id, {}).get("price"),
                    "parsed_entry": parsed_json,
                })
            except json.JSONDecodeError as e:
                results_data.append({
                    "custom_id": result.custom_id,
                    "error": f"JSON parsing failed: {e}",
                    "raw_response": response_text,
                })
        # Note: per-entry errors inside a successful batch are silently
        # skipped here. They can be found later by comparing input
        # composite_ids against custom_ids in the saved output file.

    output_path = parsed_file_for(original_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)

    return "completed"


def process_queue(in_queue_batches, log_data):
    """
    Try to retrieve every in-queue batch. Returns:
      newly_completed: list of (file_str, info) successfully retrieved
      errors:          list of (file_str, info, error_message)
    Mutates log_data in place to record completions.
    """
    newly_completed = []
    errors = []

    for file_str, info in in_queue_batches:
        try:
            status = retrieve_batch(info["batch_id"], file_str)
            if status == "completed":
                newly_completed.append((file_str, info))
                if info["batch_id"] not in log_data["completed"]:
                    log_data["completed"].append(info["batch_id"])
        except Exception as e:
            errors.append((file_str, info, str(e)))

    return newly_completed, errors


# ============================================================
# Attention items
# ============================================================

def check_attention(in_queue_batches, errors):
    """Return a list of formatted strings for things needing attention."""
    items = []
    now = datetime.now()

    # Batches stuck in queue >24h
    for file_str, info in in_queue_batches:
        try:
            submitted_dt = datetime.strptime(info["submitted_at"], "%Y%m%d-%H%M")
            age = now - submitted_dt
            if age > timedelta(hours=24):
                hours = int(age.total_seconds() / 3600)
                items.append(
                    f"⚠ Stuck in queue {hours}h: {info['batch_id']} ({info['topic']})"
                )
        except (ValueError, KeyError):
            # Skip if submitted_at is missing or malformed — not worth crashing
            pass

    # Errors during retrieval this run
    for file_str, info, err in errors:
        items.append(
            f"⚠ Retrieval failed: {info['batch_id']} ({info['topic']}) — {err}"
        )

    return items


# ============================================================
# Output formatting
# ============================================================

def format_age(timestamp_str):
    """Human-readable age of a stored ISO timestamp."""
    try:
        last = datetime.fromisoformat(timestamp_str)
    except (ValueError, TypeError):
        return "unknown"

    delta = datetime.now() - last
    if delta < timedelta(minutes=1):
        return "just now"
    if delta < timedelta(hours=1):
        return f"{int(delta.total_seconds() / 60)} minutes ago"
    if delta < timedelta(days=1):
        return f"{int(delta.total_seconds() / 3600)} hours ago"
    return f"{delta.days} days ago"


def percentage(part, total):
    """Format part/total as a clean right-aligned percentage string."""
    if total == 0:
        return "  0%"
    pct = round((part / total) * 100)
    return f"{pct:>3}%"


def print_dashboard(buckets, last_run, newly_completed, attention):
    """Print the main status dashboard."""
    total = buckets["total"]
    parsed_n = len(buckets["parsed"])
    queue_n = len(buckets["in_queue"])
    todo_n = len(buckets["not_submitted"])

    print()
    print("=" * 50)
    print("BATCH PROCESSING STATUS")
    print("=" * 50)
    print()
    print(f"  {'Total files:':<23}{total:>4}  |  100%")
    print(f"  {'Parsed & saved:':<23}{parsed_n:>4}  |  {percentage(parsed_n, total)}")
    print(f"  {'Submitted/processing:':<23}{queue_n:>4}  |  {percentage(queue_n, total)}")
    print(f"  {'Not yet submitted:':<23}{todo_n:>4}  |  {percentage(todo_n, total)}")
    print()

    # Since-last-check section
    if last_run:
        age = format_age(last_run.get("timestamp", ""))
        last_parsed = last_run.get("parsed_count", parsed_n)
        last_todo = last_run.get("not_submitted_count", todo_n)

        delta_parsed = parsed_n - last_parsed
        delta_submitted = last_todo - todo_n

        # Only show this section if anything actually changed
        if delta_parsed != 0 or delta_submitted != 0:
            print(f"  Since last check ({age}):")
            if delta_parsed > 0:
                print(f"    +{delta_parsed} newly saved")
            elif delta_parsed < 0:
                print(f"    {delta_parsed} saved (count decreased — check parsed/ folder)")
            if delta_submitted > 0:
                print(f"    +{delta_submitted} newly submitted")
            print()
    else:
        print("  (First run with new dashboard — no previous snapshot)")
        print()

    # Attention section — only appears if there's something to show
    if attention:
        print("  Needs attention:")
        for item in attention:
            print(f"    {item}")
        print()


# ============================================================
# Specific-batch mode
# ============================================================

def check_specific_batch(batch_id, log_data):
    """Check a single batch by ID (used with --batch-id flag)."""
    batch_info = None
    file_path = None
    for path, info in log_data["submitted"].items():
        if info["batch_id"] == batch_id:
            batch_info = info
            file_path = path
            break

    if not batch_info:
        print(f"❌ Batch ID {batch_id} not found in submitted batches")
        return

    print(f"Batch:     {batch_id}")
    print(f"Topic:     {batch_info['topic']}")
    print(f"Submitted: {batch_info['submitted_at']}")
    print(f"Entries:   {batch_info['entry_count']}")
    print()

    try:
        status = retrieve_batch(batch_id, file_path)
        if status == "completed":
            output = parsed_file_for(file_path)
            print(f"✅ Completed — saved to {output}")
            if batch_id not in log_data["completed"]:
                log_data["completed"].append(batch_id)
                save_log(log_data)
        elif status == "processing":
            print("⏳ Still processing")
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Check status of submitted Claude API batches"
    )
    parser.add_argument(
        "--batch-id",
        type=str,
        help="Check status of a specific batch ID",
    )
    args = parser.parse_args()

    log_data = load_log()

    # Specific-batch mode bypasses the dashboard entirely
    if args.batch_id:
        check_specific_batch(args.batch_id, log_data)
        return

    # Categorise everything based on filesystem truth
    batch_files = find_batch_files()
    buckets = categorise_batches(batch_files, log_data)

    # Try to retrieve everything currently in queue
    newly_completed, errors = process_queue(buckets["in_queue"], log_data)
    save_log(log_data)

    # Re-categorise after retrievals so the dashboard reflects the new state
    buckets = categorise_batches(batch_files, log_data)

    # Read the previous snapshot before overwriting it
    last_run = log_data.get("last_run")

    # Build the attention list (uses post-retrieval queue + this run's errors)
    attention = check_attention(buckets["in_queue"], errors)

    print_dashboard(buckets, last_run, newly_completed, attention)

    # Save the new snapshot for next run's deltas
    log_data["last_run"] = {
        "timestamp": datetime.now().isoformat(timespec="minutes"),
        "parsed_count": len(buckets["parsed"]),
        "in_queue_count": len(buckets["in_queue"]),
        "not_submitted_count": len(buckets["not_submitted"]),
    }
    save_log(log_data)


if __name__ == "__main__":
    main()
