# 06 — load onto a database branch

- **Input:** `data_reload/db_files/books.json`, `people.json`, `books2people.json`, `book_admin.json`, `prices.json`, `books2volumes.json`, split into numbered `*4loading_NN.json` files.
- **Output:** the reloaded tables on a Neon branch, later promoted. Topics were never touched.
- **Decided:** plain `executemany` inserts with `ON CONFLICT DO NOTHING`, existing keys reported before the insert, and the id sequence reset to `MAX(id)` afterwards so new rows from the app do not collide. Books first (they carry the ids), then people, then the three related tables, then books2people.
- **Logged:** `logs/book_loading_log.json` (110 files, 2 rejected rows), `logs/people_loading_log.json` (6 files, no errors).
- **Went wrong:** two books had no title and were rejected by the NOT NULL constraint. After the load, books2people was found incomplete; `load_b2p.py` was re-pointed at `fix_missing/b2p_found_list_01.json` (1,441 rows, 12 June) and `_02.json` (734 rows, 21 June). The commented-out paths in the file are that history. `books2people` has no unique constraint, so a second run of the same JSON would insert every row twice. The intended rule, one row per person per book with all role flags on it, still has 20 known exceptions in the live table; adding the constraint waits for the people-matching work that is still open.
