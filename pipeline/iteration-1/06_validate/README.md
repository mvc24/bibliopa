# 06 — validate books against their people rows

- **Input:** `data/matched/<topic>.json`, `data/people/people_records_prepped.json`, `data/people/books2people_prepped.json`.
- **Output:** `data/validated/<topic>.json` (only entries that passed), `data/people/people_records_validated.json` (only people referenced by a validated book).
- **Decided:** for every book, count authors, editors, contributors and translator in the parsed record and compare with the `books2people` rows for that `composite_id`. Total mismatch or a `unified_id` of `"oops"` fails the entry. Same total but roles swapped passes with a note.
- **Logged:** `logs/validation_log.json` per file: books, share with people rows, validated, validated with issues, failed. Full detail in `validation_failed_log.json` and `validation_report_log.json` (3 MB, not archived).
- **Went wrong:** 1,433 of 11,439 books had no `books2people` rows at all (`not_found`), SUCHLISTE worst at 21% matched. 141 failed the count check.
