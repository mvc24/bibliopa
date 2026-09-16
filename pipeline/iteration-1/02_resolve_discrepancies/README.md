# 02 — resolve the unmatched price rows

- **Input:** `data/discrepancies.json` (p rows with no exact match) and all consolidated topic files.
- **Output:** `data/logs/discrepancies_processed.json` with three lists: `resolved`, `resolved_ish`, `unresolved`.
- **Decided:** normalise, try an exact lookup, otherwise scan every consolidated entry with RapidFuzz `ratio`. Score ≥ 95 counts as resolved, 75–94 as probable, below 75 as unresolved.
- **Logged:** 1,179 discrepancies: 935 resolved, 52 probable, 192 unresolved. Runtime printed at the end.
- **Went wrong:** the scan is quadratic (every discrepancy against every entry), which is why the progress bar exists. Imports `text_matching` and `progress` from `shared/`.
