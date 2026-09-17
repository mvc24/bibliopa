# Data quality: the missing books

How 1,008 books went missing between the documents and the database, how
they were found, and what the count checks looked like.

## The symptom

In August 2026, three months after the reload, my grandfather could not
find books he knew were in the catalogue. The database held 10,919 books.
The documents had 12,614 rows. Some of that gap was expected; all of it
was not.

## The count chain

Every stage of iteration 2 writes a file keyed by `composite_id`, so
each stage can be counted and the sets compared. This is the whole
method: sets of ids, subtracted.

| Stage | Set | Count | Source |
|---|---|---|---|
| Word table rows | | 12,614 | `get_the_numbers.ipynb`, `book_counts_comparison.csv` |
| Extracted records | `raw` | 12,492 | one JSON per topic after `transform_docx.py` |
| Parsed records marked `is_reference` | `references` | 565 | flag set by the model |
| Parsed records | `parsed` | 11,498 | `data/parsed/`, after dropping references |
| Books in the database | `db` | 10,919 | export of 2026-08-07 |

Two differences, two different causes.

**12,614 − 12,492 = 122.** Rows that contain only a cross-reference to
another entry ("siehe Assmann") and produce no record. Expected, and
verified per topic: the difference is 0 for most topics and at most 14
(FRÜHES CHRISTENTUM, RELIGION ALLGEMEIN). Checked in
`book_counts_comparison.csv`.

**12,492 − 565 − 10,919 = 1,008.** Not expected. Computed as

```python
missing = raw - references - db      # sets of composite_id
len(missing)                          # 1008
```

in `10_found_them_maybe.ipynb`. Then, against `parsed`:

```python
len(parsed - db)                      # 0   → everything parsed was loaded
len(raw - references - parsed)        # 1008 → they were lost at parsing
```

So the load was complete. The Batch API had returned per-entry errors
inside batches whose overall status was "succeeded", and the retrieval
code skipped those entries without logging them.

## Why it took three months

The processing log for stage 03 records batch ids and their status, not
entry counts. A batch of 25 that came back with 22 results looked
finished. The check that would have caught it, comparing input ids with
output ids per batch, existed in iteration 1 (`06_validate`) but was not
carried into the reload. It was done by hand in the notebooks in August.

## What was done

- The 1,008 raw records were looked up by id, written to
  `data_reload/reparse_missing/missing_entries.json`, batched into 41
  files and re-parsed with the same prompt and model as the reload.
- Their people have not yet been matched, so they are not loaded. Loading
  books without people rows would put them in the same pile as the few
  hundred books already missing their `books2people` rows.

## The other known gaps

| Gap | Count | Status |
|---|---|---|
| Books with no `books2people` rows although the parse has people | a few hundred | open, `todos.md` |
| `books2people` rows holding the same person twice for one book | 20 | open; merge, then add `UNIQUE (book_id, person_id)` |
| Books rejected at load for a null title | 2 | logged in `pipeline/iteration-2/logs/book_loading_log.json` |
| Multi-person strings not split | 64 in iteration 1 | fixed by people pass 1 |

## What changed because of this

- Count per stage and per topic, and store the id sets. Totals hide the
  problem; per-topic differences of 0 are what make a difference of 14
  visible.
- A batch job's status is not the entry count. Compare ids in and out.
- The two-column table above, documents versus records per topic, is
  now the first thing produced after any extraction.
