# 01 — extract and collate the two document versions

- **Input:** the same `.docx` in two folders, `preise/` (p, older, with prices) and `keine preise/` (kp, newer text).
- **Output:** `data/consolidated/<topic>.json`, then batches of 25 under `data/batched/<topic>/`, each record with a `composite_id`.
- **Decided:** kp is the source of truth for text and topic; p is used for prices only. Exact text match, first at the same row index, then anywhere in the file. The three ERSTAUSGABEN files are merged into one topic.
- **Logged:** per file: kp rows, p rows, records created, matches found, unmatched p rows (`logs/processing_log.json`); the unmatched p rows themselves (`logs/discrepancies.json`).
- **Went wrong:** the match is exact string equality, so a row edited in kp after the prices were stripped never matches its p row. Both sides then go their own way, and the p row is the one that gets noticed.

## Why there were two versions

My grandfather had kept price estimates in his catalogue for years.
Antiquarian dealers dislike being handed a seller's own estimates, and he
wanted a version he could give them on a stick, so a few months before the
project started he went through every document and removed the prices. That
produced "keine Preise" (kp). While he was in there he also corrected things
he noticed and moved entries from one topic file to another, which is why kp
is the authoritative text — but there was no guarantee that nothing relevant
had also changed in "Preise" (p), so neither file could be discarded.

## What happens to a row that does not match

Every kp row produces a record, matched or not. An unmatched one is written
with `price: None` and carries on into parsing — it is never a discrepancy.
A discrepancy is a **p** row that no kp row matched: present in the older
priced version, not found in the authoritative one. That is why the count
matters. It is not "rows that lost their price", it is "entries my
grandfather could see in one version and not the other".

Both numbers follow from the same subtraction:

| | |
|---|---|
| kp rows | 12,573 |
| p rows | 12,700 |
| records created (one per kp row) | 12,573 |
| matched, price taken from p | 11,544 |
| kp rows kept with no price | 1,029 |
| discrepancies (p rows, unmatched) | 1,156 |

`discrepancies.json` is opened, extended and written back, never reset, so a
partial re-run appends its rows a second time. The file holds 1,179 rows
against the log's 1,156.
