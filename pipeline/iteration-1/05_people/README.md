# 05 — people: split, then deduplicate

- **Input:** `database/in_progress/collect_people.json`, one row per person mention as the parser returned it (17,722 rows).
- **Output:** pass 1 results (`results_pass1_*.json`, multi-person strings split), pass 2 results (`results_pass2_*.json`, every row with a `unified_id` and a `variants` list).
- **Decided:** two API passes, because splitting and deduplicating in one prompt gave results that could not be checked. Pass 1 only takes rows with no `family_name` and an " und " or " u. " in the name (64 rows, 3 batches). Pass 2 groups rows by normalised surname, so each request sees all spellings of one name together (17,702 rows, 7,076 surname groups, 252 batches, about 70 rows each). Unsure cases get `unified_id: "oops"`. `normalise_people.py` is the earlier, non-API attempt at grouping.
- **Logged:** `logs/pass1_preparation.log`, `logs/pass2_preparation.log`, plus a tracking file per pass with batch ids and retrieval status.
- **Went wrong:** `people_batch_processor.py` submits, `check_people_status.py` retrieves; both had to be run repeatedly by hand. Cost about $6, runtime about 3h45.
