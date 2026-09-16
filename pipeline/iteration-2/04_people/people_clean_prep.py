import json
from pathlib import Path

project_root = Path(__file__).parent.parent

people_file = project_root / "data/from db/people.json"
batch_output_dir = project_root / "database/in_progress/clean_batches"
log_file = project_root / "database/in_progress/clean_prep.log"

BATCH_SIZE = 500


def main():
    print(f"Loading people from {people_file}...")
    with open(people_file, "r", encoding="utf-8") as f:
        people = json.load(f)

    print(f"Loaded {len(people)} people")

    batch_output_dir.mkdir(parents=True, exist_ok=True)

    batches = [people[i:i + BATCH_SIZE] for i in range(0, len(people), BATCH_SIZE)]

    print(f"Created {len(batches)} batches of up to {BATCH_SIZE} entries")

    for idx, batch in enumerate(batches, start=1):
        batch_file = batch_output_dir / f"batch_clean_{idx:02d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"  Saved {batch_file.name} ({len(batch)} entries)")

    summary = {
        "total_people": len(people),
        "batches_created": len(batches),
        "batch_size": BATCH_SIZE,
        "output_directory": str(batch_output_dir)
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nSummary saved to {log_file}")
    print(f"Batches ready for Operation A (clean existing people)!")
    print(f"  Total batches: {len(batches)}")
    print(f"  Total requests: {len(people)}")


if __name__ == "__main__":
    main()
