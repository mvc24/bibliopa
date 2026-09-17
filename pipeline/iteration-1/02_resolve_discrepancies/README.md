# 02 — resolve the unmatched price rows

- **Input:** `data/discrepancies.json` (p rows with no exact match) and all consolidated topic files.
- **Output:** `data/logs/discrepancies_processed.json` with three lists: `resolved`, `resolved_ish`, `unresolved`.
- **Decided:** normalise, try an exact lookup, otherwise scan every consolidated entry with RapidFuzz `ratio`. Score ≥ 95 counts as resolved, 75–94 as probable, below 75 as unresolved.
- **Logged:** 1,179 discrepancies: 935 resolved, 52 probable, 192 unresolved. Runtime printed at the end.
- **Went wrong:** the scan is quadratic (every discrepancy against every entry), which is why the progress bar exists. Imports `text_matching` and `progress` from `shared/`.

## The results were never applied

The lookup is built from every consolidated topic at once, not one topic at
a time, so a p row that had been moved to a different topic file is found.
935 of the 1,179 were located this way — most of them had not gone missing
at all, they had moved.

But `resolve_discrepancies()` only writes `matched_topic` and `matched_price`
into its own log. Nothing reads that log back into `data/consolidated/`, so
no price was restored and no topic corrected. The stage diagnosed the
problem and stopped there.

That left 1,156 entries (see stage 01 for the count) that my grandfather
could see were missing from the version he was being shown. Feeding the
results back by hand was possible but slow, and by then he had gone on
working in a document that had prices again, without ever consolidating the
two versions. Re-reading a single corrected document was cheaper than
reconciling the two — which is what iteration 2 is.
