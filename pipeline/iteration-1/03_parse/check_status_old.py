import json
import argparse
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Load environment variables and create API client
load_dotenv()
client = anthropic.Anthropic()

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

def retrieve_batch_results(batch_id, original_file):
    # Check status first
    batch_status = client.messages.batches.retrieve(batch_id)
    print("Current status:", batch_status.processing_status)

    # If not ready, return without processing
    if batch_status.processing_status != "ended":
        return {"status": "processing", "batch_id": batch_id}

    # Only get results ONCE when ready
    batch_results = client.messages.batches.results(batch_id)
    results_list = list(batch_results)  # Convert to list immediately

    # Convert results to JSON-serializable format
    results_data = []
    for result in results_list:  # Use the list we already created
        if result.result and result.result.type == "succeeded":  # Changed from "message" to "succeeded"
            # Extract the text content from the message
            response_text = result.result.message.content[0].text  # Changed path

            # Strip markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json\n", "").replace("\n```", "")

            try:
                # Parse the actual JSON
                parsed_json = json.loads(response_text)
                result_data = {
                    "custom_id": result.custom_id,
                    "parsed_entry": parsed_json
                }
            except json.JSONDecodeError as e:
                result_data = {
                    "custom_id": result.custom_id,
                    "error": f"JSON parsing failed: {e}",
                    "raw_response": response_text
                }

            results_data.append(result_data)

    # Save results to file (single file creation)

    filename = Path(original_file).stem
    filepath = f"data/parsed/batch_{filename}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {filepath}")
    print(f"Number of results: {len(results_data)}")

    return {
        "status": "completed",
        "batch_id": batch_id,
        "output_file": filepath,
        "results_count": len(results_data)
    }

def check_specific_batch(batch_id):
    """Check status of a specific batch by ID"""
    log_data = load_log()

    # Find batch info
    batch_info = None
    batch_file_path = None
    for file_path, submission_info in log_data["submitted"].items():
        if submission_info["batch_id"] == batch_id:
            batch_info = submission_info
            batch_file_path = file_path
            break

    if not batch_info:
        print(f"❌ Batch ID {batch_id} not found in submitted batches")
        return

    print(f"Checking batch: {batch_id}")
    print(f"Topic: {batch_info['topic']}")
    print(f"Submitted: {batch_info['submitted_at']}")
    print(f"Entries: {batch_info['entry_count']}")
    print()

    try:
        result = retrieve_batch_results(batch_id, batch_file_path)

        if result["status"] == "completed":
            print(f"✅ Status: COMPLETED")
            print(f"Output file: {result['output_file']}")
            print(f"Results count: {result['results_count']}")

            # Update log if not already marked complete
            if batch_id not in log_data["completed"]:
                log_data["completed"].append(batch_id)
                save_log(log_data)
                print("✓ Marked as completed in progress log")

        elif result["status"] == "processing":
            print(f"⏳ Status: PROCESSING")
            print("Check again later")

        else:
            print(f"❓ Status: {result['status']}")

    except Exception as e:
        print(f"❌ Error checking batch: {e}")

def check_all_batches():
    """Check status of all submitted batches"""
    print("Checking status of all submitted batches...")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")

    log_data = load_log()
    completed_batch_ids = set(log_data["completed"])

    if not log_data["submitted"]:
        print("No submitted batches found.")
        return

    print(f"\n=== BATCH STATUS CHECK ===")

    newly_completed = 0
    still_processing = 0
    errors = 0

    for file_path, submission_info in log_data["submitted"].items():
        batch_id = submission_info["batch_id"]
        topic = submission_info["topic"]

        if batch_id in completed_batch_ids:
            print(f"✅ Already completed: {batch_id} ({topic})")
            continue

        try:
            print(f"🔍 Checking: {batch_id} ({topic})")
            result = retrieve_batch_results(batch_id, file_path)

            if result["status"] == "completed":
                print(f"  ✅ COMPLETED: {result['output_file']} ({result['results_count']} results)")
                log_data["completed"].append(batch_id)
                newly_completed += 1

            elif result["status"] == "processing":
                print(f"  ⏳ Still processing...")
                still_processing += 1

            else:
                print(f"  ❓ Status: {result['status']}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            log_data["failed"].append({
                "batch_id": batch_id,
                "error": str(e),
                "timestamp": timestamp
            })
            errors += 1

    # Save updated log
    save_log(log_data)

    # Final summary
    print(f"\n=== STATUS SUMMARY ===")
    print(f"Total submitted batches: {len(log_data['submitted'])}")
    print(f"Completed batches: {len(log_data['completed'])}")
    print(f"Failed batches: {len(log_data['failed'])}")
    print(f"Still processing: {len(log_data['submitted']) - len(log_data['completed'])}")

    print(f"\nThis check:")
    print(f"  Newly completed: {newly_completed}")
    print(f"  Still processing: {still_processing}")
    print(f"  Errors encountered: {errors}")

    if still_processing > 0:
        print(f"\n⏰ Run this script again in 10-15 minutes to check for more completed batches.")

def main():
    parser = argparse.ArgumentParser(
        description='Check status of submitted Claude API batches'
    )
    parser.add_argument(
        '--batch-id',
        type=str,
        help='Check status of specific batch ID (if not provided, checks all batches)'
    )

    args = parser.parse_args()

    print("Claude API Batch Status Checker")
    print("=" * 40)

    if args.batch_id:
        check_specific_batch(args.batch_id)
    else:
        check_all_batches()

if __name__ == "__main__":
    main()
