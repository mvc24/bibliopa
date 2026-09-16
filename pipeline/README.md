# The Word-to-database migration, as it was run

This folder is a readable archive, not a package. Nothing in it runs end to
end any more: paths point at data folders that are not in the repo, and the
scripts were edited between runs. It is here so the migration can be read in
the order it happened, with the counts and logs as they were produced.

The source was about 50 Word documents, one per topic, each a table with one
bibliographic entry per row. The target is the PostgreSQL schema built by
`alembic/`. The transformation was done twice.

## Iteration 1 — September 2025 to January 2026

Two non-identical versions of the catalogue existed: "keine Preise" (kp, the
newer text) and "Preise" (p, older but with prices). They had to be collated
before parsing. After parsing was done and paid for, a third, newer set of
documents arrived, so the parsed records were matched back onto the new text
instead of being re-parsed.

| stage | what | when | counts |
|---|---|---|---|
| 01 | read both versions, take text from kp and prices from p, batch | 2025-09-08 – 09-12 | first 16 files: 1,016 rows, 956 prices matched, 79 unmatched p rows |
| 02 | fuzzy-resolve the unmatched p rows against everything | 2025-09-29 | 1,179 discrepancies: 935 resolved (≥95), 52 probable (75–94), 192 unresolved |
| 03 | parse every batch with the Claude Batch API | 2025-09-11 – 09-25 | 25 entries per batch, `claude-sonnet-4-20250514`, about $200 |
| 04 | match parsed records onto the newer documents | 2025-12-14 – 12-17 | flags `topic_changed`, `price_changed` |
| 05 | people: split multi-person strings, then deduplicate by surname | 2025-10-06 – 10-09 | 17,722 person records; 64 split in 3 batches; 17,702 into 252 batches over 7,076 surname groups |
| 06 | validate books against their people rows before loading | 2026-01-15 | 48 files, 11,439 books: 9,830 validated, 35 with role mismatches, 141 failed, 1,433 without people rows |
| 07 | load: first an orchestrator script, then Alembic data migrations | 2026-01-20 – 01-26 | topics → books → people → related tables |

The result was deployed and used.

## Iteration 2 — April to August 2026

A single corrected version of all documents, marked up by hand: `! ` at the
start of an edited row, `AUS! ` at the start of a removed one. The schema was
also adapted to what the first iteration had shown: `isbn` went (it was never
going to be researched); `is_active` came in as a number, not a boolean, so
that entries with certain API flags could be held back from display with
room for finer levels later; and name particles were split into
`name_prefix`, `name_particles` and `name_suffix`, because one field for all
of them made conditional rendering and sorting impractical. Rather than
patch, the whole thing was re-extracted, re-parsed and reloaded onto a Neon
database branch, because the first version was live and in use.

| stage | what | when | counts |
|---|---|---|---|
| 01 | read the documents, drop `AUS! ` rows, strip `! `, join line breaks with ` \|\| ` | 2026-04-26 – 04-28 | 12,614 document rows → 12,492 records; the 122 missing are cross-reference rows |
| 02 | batch and assign `composite_id` | 2026-04-26 | `topic_index_batch_totalbatches` |
| 03 | parse with a rewritten prompt: flags instead of a confidence score | 2026-04 – 05 | `claude-sonnet-4-6`, prompt cached |
| 04 | people: match onto the existing `people_variants`, clean the rest, resolve the "nopes" | 2026-05-01 – 05-13 | 9,060 unique names, 5,595 matched (62%); 7,817 people cleaned in 16 batches; 1,223 nopes in 41 batches |
| 05 | flatten parsed JSON into per-table records | 2026-05 | 11,498 records after dropping references |
| 06 | load with `executemany` onto a database branch | 2026-05-20 – 05-22 | 110 book files, 2 rows rejected (null title); books2people rows found missing, 1,441 + 734 added in June |

Entries that had gone missing between the two runs were hunted down and
re-parsed in August 2026 (see `docs/data-quality.md`).

## Layout

Each stage folder has a `README.md` with the same five lines: input, output,
what it decided, what it logged, what went wrong. `logs/` holds the run logs
that survived, unedited apart from replacing the home directory in paths.
`shared/` holds the two helpers several stages import.

The Alembic data migrations under `iteration-1/07_load/` are copies. The live
ones in `alembic/versions/` are no-ops with a pointer here, so that
`alembic upgrade head` builds an empty schema without needing the data files.
