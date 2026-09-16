# 07 — load into PostgreSQL

- **Input:** `data/validated/<topic>.json`, `data/people/people_records_validated.json`, the `.docx` filenames (for topics).
- **Output:** the first production database: topics, books, people, books2people, book_admin, prices, books2volumes.
- **Decided:** the first attempt, `initial_load/db_orchestrator_old.py` with `load_entries_old.py`, inserted row by row per file and could not recover from a partial run. It was replaced by four Alembic data migrations (`alembic_data_migrations/`), each importing a prep function from `initial_load/` and calling `op.bulk_insert`. Load order topics → books → people → related tables; database ids are read back after the books insert to fill the foreign keys (`prep_related_tables.py`). Topics are the document names (`get_topics.py`), numbered in file order; `topic_slugs.py` derives the URL slug the same way `01` did.
- **Logged:** `logs/data_loading_log.json` from the orchestrator era; the Alembic runs printed progress only.
- **Went wrong:** moving from the local database to Neon reshuffled topic ids, so every book's `topic_id` had to be remapped by hand from a mapping file (`fix_topic_ids.py`). That is why the topics table is never truncated in iteration 2. `load_entries.py` is an intermediate version that was never run in full.
