# 01 — extract and collate the two document versions

- **Input:** the same `.docx` in two folders, `preise/` (p, older, with prices) and `keine preise/` (kp, newer text).
- **Output:** `data/consolidated/<topic>.json`, then batches of 25 under `data/batched/<topic>/`, each record with a `composite_id`.
- **Decided:** kp is the source of truth for text and topic; p is used for prices only. Exact text match, first at the same row index, then anywhere in the file. The three ERSTAUSGABEN files are merged into one topic.
- **Logged:** per file: kp rows, p rows, records created, matches found, unmatched p rows (`logs/processing_log.json`); the unmatched p rows themselves (`logs/discrepancies.json`).
- **Went wrong:** only the 16 smallest files have a surviving log entry; the log for the remaining files was overwritten. Price matching was exact-string only, so every edited row lost its price and landed in the discrepancies.
