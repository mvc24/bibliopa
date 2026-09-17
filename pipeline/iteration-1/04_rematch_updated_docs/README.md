# 04 — match parsed records onto the newer documents

- **Input:** the newer documents, already read into `data/raw/prepped/<topic>.json`; every parsed result under `data/parsed/`; the list of corrupt results and their hand-cleaned replacements.
- **Output:** `data/matched/<topic>.json` keyed by `composite_id`, and `data/processing/unmatched_entries.json`.
- **Decided:** re-parsing would have cost another 200 €, so the parsed records are kept and matched onto the new text by normalised `original_entry`. Rows starting with `AUS!` are skipped. Where topic or price differ, the new value wins and `topic_changed` / `price_changed` is set to 1.
- **Logged:** per file: entries, matched, unmatched, printed to the console.
- **Went wrong:** the match is exact after normalisation, so every edited entry is unmatched. These are the origin of the missing-entries hunt in iteration 2.
