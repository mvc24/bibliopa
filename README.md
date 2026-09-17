# bibliopa

My grandfather, a retired librarian, catalogued his private library for
decades in about 50 Word documents, one per topic, one table row per book.
bibliopa moved that catalogue into PostgreSQL and a web app he used himself.

**Live:** https://bibliopa.vercel.app · **Project page (DE/EN):**
https://bibliopa.vercel.app/project

This is a portfolio project. The migration was done twice, and the second
run exists because of what the first one got wrong. Both runs are kept in
the repo as they were, with their counts and logs. The evidence is
traceability: one book can be followed from its Word row to its database
row (`docs/trace.md`).

## Where to look

| If you want to see | Open |
|---|---|
| the whole story in five minutes | this file |
| both migration runs, stage by stage, with counts | [`pipeline/README.md`](pipeline/README.md) |
| one real book followed through every stage | [`docs/trace.md`](docs/trace.md) |
| how ~1,000 books went missing and were found | [`docs/data-quality.md`](docs/data-quality.md) |
| how 17,722 person mentions became 8,947 people | [`docs/entity-resolution.md`](docs/entity-resolution.md) |
| the tables, and what changed between the runs | [`docs/schema.md`](docs/schema.md) |
| how an LLM was used: in the pipeline, and as a tool | [`docs/working-with-ai.md`](docs/working-with-ai.md) |
| the prompt that parsed 12,000 German catalogue entries | [`pipeline/iteration-2/03_parse/`](pipeline/iteration-2/03_parse/) |
| the web app | [`frontend/`](frontend/) |

## What it is

- **Source:** ~50 `.docx` files, each a table, one bibliographic entry per
  row, written over decades in RAK cataloguing style with hand-typed
  abbreviations, prices and cross-references.
- **Target:** PostgreSQL with `books`, `people`, `books2people`,
  `book_admin`, `prices`, `books2volumes`, `topics`; a Next.js app on top.
- **Transformation:** Python. Extract rows with `python-docx`, parse each
  entry into JSON with the Claude Batch API, deduplicate people with
  RapidFuzz and a second API pass, validate, load with `executemany`.
- **Constraints:** one person, no reviewers, learning Python while doing
  it; a 90-year-old end user with low vision and a tremor; an API budget
  of a few hundred euros.

## Why twice

**Iteration 1 (September 2025 to January 2026).** Two non-identical
versions of the catalogue existed: one with prices, one without, made by
hand from the first and then edited further. They had to be collated
before parsing. Collation matched 11,544 rows exactly and left 1,156
priced rows it could not place. A second stage located 935 of them by fuzzy
matching, but its results were never written back. The database went
live with those entries missing, which my grandfather noticed.

**Iteration 2 (April to August 2026).** Rather than reconcile two
versions, he corrected one document set and marked every edited row with
`! ` and every removed row with `AUS! `. That set was re-extracted,
re-parsed with a rewritten prompt and reloaded onto a database branch,
because the first version was live. People were matched onto the existing
people table instead of being deduplicated again.

Full stage tables with dates and counts: [`pipeline/README.md`](pipeline/README.md).

## Numbers

| | |
|---|---|
| Word documents | 49 (46 topics; one topic split over three files) |
| Table rows in the documents | 12,614 |
| Records after extraction | 12,492 (122 rows are cross-references only) |
| Records after parsing, references dropped | 11,498 |
| Books in the database | 10,919 |
| Books found missing in August 2026, re-parsed, not yet loaded | 1,008 |
| Person mentions in the parsed data | 17,722 |
| People in the database | 8,947 |
| Parsing cost, both runs | about 200 € (iteration 2 not recorded separately) |
| People deduplication, API | about 6 €, 252 batches, 3h45 |

## Three decisions and what they cost

1. **A human-readable id on every record.** `composite_id` is
   `topic_index_batch_totalbatches`, assigned at batching time and kept
   through parsing, loading and the app. It is what made the trace, the
   missing-books hunt and the reload possible. Cost: the id encodes the
   row position, so 92% of books have a different `composite_id` in the
   two runs and the runs cannot be joined on it. They are joined on entry
   text instead.
2. **Flags instead of a confidence score.** Iteration 1 asked the model
   for `parsing_confidence` and `needs_review`, which turned out to be
   unreviewable. Iteration 2 asks for six booleans, each with a written
   reason, and lets the model correct obvious typos but mark that it did.
   Cost: a full re-parse, and a review queue that still needs building.
3. **Keep the existing people.** In the reload, new person mentions were
   matched onto the 7,817 people already in the database rather than
   deduplicated from scratch. Cost: only 62% matched exactly, so a third
   API pass with context was needed, and a few hundred books still have no
   people rows.

## Status

Delivered and used. My grandfather browsed, searched and added entries
through the app for several months. In 2026 he decided to sell the
collection; the app is now the catalogue that goes with the sale, and the
focus shifted from structured detail to "every book is visible, with its
original entry text".

Open data work, in order (`todos.md`): load the 1,008 re-parsed books
after matching their people; merge the 20 `books2people` rows that hold
the same person twice, then add the unique constraint; run the fixed
Splink model on the remaining unmatched names (see
`docs/entity-resolution.md`).

## Known limitations

- The author filter needs three characters, so two-letter surnames ("Ku")
  cannot be filtered.
- Full-text search is a substring match on the original entry, so "Ku"
  also hits "Kunst", "Kultur" and every other word containing it.
- Multi-volume works are stored but not yet displayed as volumes.
- Nothing is ever deleted: removed books are soft-deleted (`is_removed`).

## Running it

The migration is an archive, not a package: `pipeline/` reads in order but
does not run end to end (see its README). What does run:

```bash
# database schema, empty
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
printf 'DATABASE_URL=postgresql://user:password@localhost/bibliopa\nANTHROPIC_API_KEY=...\n' > .env
alembic upgrade head
```

```bash
# web app
cd frontend
npm install
npm run dev                 # http://localhost:3000, needs frontend/.env.local
```

`npm run dev` uses `--webpack`; Turbopack runs out of memory on the
development machine.

## Stack

Python 3.14 · `python-docx` · `anthropic` (Batch API) · RapidFuzz ·
Splink (experiment) · psycopg · SQLAlchemy · Alembic · PostgreSQL on Neon ·
Next.js 16 · React 19 · React Aria Components · Tailwind 4 · next-auth ·
Vercel
