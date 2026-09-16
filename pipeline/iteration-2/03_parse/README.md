# 03 — parse with the rewritten prompt

- **Input:** batch files under `data/raw/batched/<topic>/`.
- **Output:** `data/parsed/batch_<topic>_<n>-<total>.json`, each result with `custom_id`, `price` (carried over from the input, no longer sent to the model) and `parsed_entry`.
- **Decided:** the confidence score and `needs_review` of iteration 1 are gone. Instead six boolean flags: `is_reference`, `corrected_by_api`, `missing_person`, `multiple_editions`, `api_concerned`, `problematic_multi_volume`, each requiring a `verification_notes` explanation. People are returned as a single `display_name`; splitting names is left to stage 04. Model `claude-sonnet-4-6`, system prompt cached.
- **Logged:** `data/logs/batch_progress.json`; `check_status.py` trusts the filesystem over the log and prints a dashboard with stuck batches.
- **Went wrong:** per-entry API errors inside a successful batch are silently skipped on retrieval; they were found afterwards by comparing input ids with output ids. The copies of `batch_processor.py` and `check_status.py` in `api/` were later edited for the August 2026 re-parse of missing entries; these are the May 2026 versions.
