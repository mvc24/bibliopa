# 05 — flatten parsed JSON into per-table records

- **Input:** `data/parsed/batch_*.json`, `data/from db/topics.json` (the untouched topics table).
- **Output:** `data/prepped/<topic>.json` keyed by `composite_id`, each holding `books_data`, `admin_data`, `price_data`, `volumes_data`; `database/people_extracted.json` for stage 04.
- **Decided:** references (`is_reference`) produce no record. `is_active` is derived from the flags: 0 when `api_concerned` or `problematic_multi_volume`, 2 when corrected, missing a person, multiple editions or any note, 1 otherwise. ` || ` becomes a line break again and `<<` `>>` become German quotes. Topic id comes from the existing table by slug, never regenerated.
- **Logged:** `data/logs/prep_log.json`: entries and people per topic, totals, and a `critical` list for records missing a field or a topic. 11,498 entries, 0 critical.
- **Went wrong:** nothing recorded.
