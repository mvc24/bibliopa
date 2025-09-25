import json
from pathlib import Path
from pprint import pp
from re import sub


batch_log = Path("data/logs/batch_progress.json")
log = Path("data/logs/data_loading_log.json")
parsed_folder = Path("data/parsed")
count_files = list(parsed_folder.iterdir())
# pp(f"Number of files in parsed: {len(count_files)}")


"""json structure:

{
  "submitted": {
    "data/batched/symbolkunde/symbolkunde_1-2.json": {
      "batch_id": "msgbatch_019beNjKvjn6q31m7x7r3nzR",
      "topic": "symbolkunde",
      "submitted_at": "20250911-2241",
      "entry_count": 25
    },
    ...
    "completed": [
    "msgbatch_019beNjKvjn6q31m7x7r3nzR",
    "msgbatch_01Y3pEMStCQmdZUdAizds63Q",
    "msgbatch_018Uc1ekR2LfQPTMcyvp5MK7",
    ...
    ],
  "failed": []
}

"""

# def count_consolidated_entries():
#     folder = Path("data/consolidated")
#     total_entries = 0
#     counts = []
#     # file_paths = list(folder.iterdir())
#     for file in list(folder.iterdir()):
#         file_path = file

#         with open(file_path, "r") as f:
#             content = json.load(f)
#             count = len(content)
#             counts.append(count)
#             total_entries += count


#         # pp(filename)
#         # pp(f"count: {count}")

#         total = 0

#     for count in counts:
#         # pp(f"total = {total}")
#         previous_total = total
#         total += count
#         pp(f"{previous_total} + {count} is {total}.")


#     pp(total)


# count_consolidated_entries()

def count_entries():
    completed = []
    with open (batch_log, "r") as f:
        batches = json.load(f)
        batch_count = 0
        batch_entry_count = 0
        count_unique_batch_entries = 0

    with open(log, "r") as f:
        entries = json.load(f)
        entry_count = 0
        corrupt_count = 0
        unique_count = 0

        for index, entry in enumerate(entries):
            entry_count += entry["entry_count"]
            corrupt_count += entry["corrupt_entries_found"]
            # pp(entry_count)
            # processed = len(entries)

        for batch in batches.items():
            submitted = batches["submitted"]
            completed = batches["completed"]


            completed_total = len(batches["completed"])

            batch_count = len(submitted)

            for submitted_entry in submitted.values():
                batch_entry_count += submitted_entry["entry_count"]
                batch_id = submitted_entry.get("batch_id")
                count = submitted_entry.get("entry_count")

            # unique_batches = [id for id in completed if batch_id in completed]
                if batch_id in completed:
                    count_unique_batch_entries += count

            # nr_unique = len(unique_batches)
            # unique_count +=
            # for batch_id in completed.values():

    # pp(f"batch_id{batch_id}")
    # pp(f"count_unique_batch_entries: {count_unique_batch_entries}")
    # pp(f"processed {processed} files")
    # pp(f"entry count = {entry_count}")
    # pp(f"corrupt = {corrupt_count}")
    # pp(f"batches submitted = {batch_count}")
    # pp(f"entries submitted = {batch_entry_count}")
    # pp(f"ids completed = {completed_total}")
    # pp(524 * 25)
    # pp(type(completed))
    # # pp(f"completed = {completed}")
    # pp(f"unique = {unique_count}")


# TODO: This doesn't add up:
# 'Number of files in parsed: 75'
# 'entry count = 1501'
# 'corrupt = 45'
# 'batches submitted = 525'
# 'entries submitted = 37719'
# 'ids completed = 524'
#  assuming each batch file has 25 entries: 13100 total
# 'count_unique_batch_entries: 37644'


# count_entries()
