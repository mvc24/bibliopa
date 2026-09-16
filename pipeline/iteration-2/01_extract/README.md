# 01 — extract the corrected documents

- **Input:** one folder of `.docx`, `data/raw/original/`, the corrected single version of the catalogue.
- **Output:** `data/raw/prepped/<topic>.json`, one record per row: `text`, `source`, `price`, `topic`, `topic_normalised`.
- **Decided:** rows starting with `AUS! ` are removed entries and are dropped. A leading `! ` marks an edited row and is stripped. Line breaks inside a cell become ` || ` so the parser can see the structure. Curly quotes are unified. Price is pulled out with the same regex as iteration 1.
- **Logged:** `data/logs/processing_log.json`: timestamp, topic, entries created, per file. The per-topic comparison with the document row counts is `logs/book_counts_comparison.csv`.
- **Went wrong:** nothing in the script; 12,614 rows became 12,492 records, and the 122 difference was traced to rows holding only a cross-reference.
