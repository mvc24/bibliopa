import anthropic
from dotenv import load_dotenv
import json
from pathlib import Path
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

# Create connection to API
client = anthropic.Anthropic()

def check_batch_status(batch_id):
    """
    Check the status of a single batch.
    """
    try:
        batch = client.messages.batches.retrieve(batch_id)
        return {
            "id": batch.id,
            "processing_status": batch.processing_status,
            "request_counts": {
                "processing": batch.request_counts.processing,
                "succeeded": batch.request_counts.succeeded,
                "errored": batch.request_counts.errored,
                "canceled": batch.request_counts.canceled,
                "expired": batch.request_counts.expired
            },
            "ended_at": batch.ended_at,
            "results_url": batch.results_url if hasattr(batch, 'results_url') else None
        }
    except Exception as e:
        return {"id": batch_id, "error": str(e)}


def retrieve_results(batch_id, output_path):
    """
    Retrieve and save results for a completed batch.
    """
    try:
        # Get the batch results
        results = client.messages.batches.results(batch_id)

        parsed_results = []
        for result in results:
            # Each result contains the custom_id and the response
            custom_id = result.custom_id

            if result.result.type == "succeeded":
                # Extract the JSON content from the response
                content = result.result.message.content[0].text
                try:
                    # Parse the JSON array returned by Claude
                    person_entries = json.loads(content)

                    # Add custom_id to each entry for tracking
                    if isinstance(person_entries, list):
                        for entry in person_entries:
                            entry["_source_custom_id"] = custom_id
                        parsed_results.extend(person_entries)
                    else:
                        # If not a list, something went wrong
                        parsed_results.append({
                            "unified_id": "oops",
                            "_source_custom_id": custom_id,
                            "_error": "Response was not an array"
                        })
                except json.JSONDecodeError as e:
                    parsed_results.append({
                        "unified_id": "oops",
                        "_source_custom_id": custom_id,
                        "_error": f"JSON decode error: {str(e)}",
                        "_raw_content": content
                    })
            else:
                # Handle error cases
                parsed_results.append({
                    "unified_id": "oops",
                    "_source_custom_id": custom_id,
                    "_error": f"API error: {result.result.type}"
                })

        # Save results
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_results, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "entry_count": len(parsed_results),
            "output_path": str(output_path)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """
    Check status of tracked batches for Pass 1 or Pass 2.
    Usage:
        python check_people_status.py pass1  # Check Pass 1 status
        python check_people_status.py pass2  # Check Pass 2 status
    """
    # Determine which pass to check
    if len(sys.argv) < 2:
        print("Usage: python check_people_status.py [pass1|pass2]")
        print("  pass1: Check Pass 1 (splitting) batch status")
        print("  pass2: Check Pass 2 (deduplication) batch status")
        return

    pass_type = sys.argv[1].lower()

    if pass_type == "pass1":
        tracking_file = Path("database/in_progress/pass1_batch_tracking.json")
        results_dir = Path("database/in_progress/pass1_results")
        batch_pattern = "batch_split_"
        results_prefix = "results_pass1_"
        pass_name = "Pass 1"
    elif pass_type == "pass2":
        tracking_file = Path("database/in_progress/pass2_batch_tracking.json")
        results_dir = Path("database/in_progress/pass2_results")
        batch_pattern = "batch_dedup_"
        results_prefix = "results_pass2_"
        pass_name = "Pass 2"
    else:
        print(f"Unknown pass type: {pass_type}")
        print("Use 'pass1' or 'pass2'")
        return

    print(f"=== {pass_name} Status Check ===\n")

    results_dir.mkdir(parents=True, exist_ok=True)

    if not tracking_file.exists():
        print(f"No tracking file found at {tracking_file}")
        return

    # Load tracking data
    with open(tracking_file, "r") as f:
        tracking_data = json.load(f)

    print(f"Checking status of {len(tracking_data)} batches...\n")

    updated = False

    for batch_info in tracking_data:
        batch_id = batch_info["batch_id"]
        batch_file = Path(batch_info["file_path"]).name

        print(f"Batch: {batch_file}")
        print(f"  ID: {batch_id}")

        # Check status
        status = check_batch_status(batch_id)

        if "error" in status:
            print(f"  Error: {status['error']}")
            continue

        current_status = status["processing_status"]
        print(f"  Status: {current_status}")

        # Update tracking data
        batch_info["last_checked"] = datetime.now().isoformat()
        batch_info["processing_status"] = current_status
        batch_info["request_counts"] = status["request_counts"]

        # If completed and results not yet retrieved
        if current_status == "ended" and "results_retrieved" not in batch_info:
            print(f"  Retrieving results...")

            # Create output filename based on batch file
            output_file = results_dir / batch_file.replace(batch_pattern, results_prefix)

            result = retrieve_results(batch_id, output_file)

            if result["success"]:
                print(f"  ✓ Retrieved {result['entry_count']} entries")
                print(f"  Saved to: {result['output_path']}")
                batch_info["results_retrieved"] = True
                batch_info["results_path"] = result["output_path"]
                batch_info["result_count"] = result["entry_count"]
                updated = True
            else:
                print(f"  Error retrieving results: {result['error']}")

        print()

    # Save updated tracking data
    if updated:
        with open(tracking_file, "w") as f:
            json.dump(tracking_data, f, ensure_ascii=False, indent=2)
        print(f"Updated tracking file saved")

    # Summary
    completed = sum(1 for b in tracking_data if b.get("processing_status") == "ended")
    retrieved = sum(1 for b in tracking_data if b.get("results_retrieved"))

    print(f"\nSummary:")
    print(f"  Total batches: {len(tracking_data)}")
    print(f"  Completed: {completed}")
    print(f"  Results retrieved: {retrieved}")


if __name__ == "__main__":
    main()
