# 02 — batch and assign composite ids

- **Input:** `data/raw/prepped/<topic>.json`.
- **Output:** `data/raw/batched/<topic>/<topic>_<n>-<total>.json`, 25 records each.
- **Decided:** `composite_id = <topic>_<index>_<batch>_<total_batches>`, the same scheme as iteration 1, so a record can be traced back to its document row and forward to its database row. The three ERSTAUSGABEN files are merged before batching.
- **Logged:** filenames printed as saved.
- **Went wrong:** nothing recorded.
