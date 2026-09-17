# 03 — parse every batch with the Claude Batch API

- **Input:** batch files under `data/batched/<topic>/`, 25 entries each, with `composite_id`, `price`, `topic`, `text`.
- **Output:** `data/parsed/batch_<topic>_<n>-<total>.json`, one result per entry: `custom_id` and `parsed_entry` (the schema in the system prompt), or `error` + `raw_response`.
- **Decided:** one API request per entry, the whole batch file as one Batch API job, at most 15 jobs per run. Model `claude-sonnet-4-20250514`, temperature 0. The prompt asks for a `parsing_confidence` and `needs_review` on every record.
- **Logged:** `data/logs/batch_progress.json`: submitted jobs keyed by file, completed batch ids, failed submissions.
- **Went wrong:** the API sometimes returned a list instead of an object, or JSON that would not parse; both cases were handled downstream (`04`). Cost about 200 € for the full run. The files are named `*_old.py` because the reload reused the names.
