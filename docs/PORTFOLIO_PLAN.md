# Bibliopa: from working project to portfolio piece

## Context

Review done 2026-09-15 across the project folder and `../bibliopa_backup_stuff`.
Findings are in the conversation; this file is the resulting plan.

What the project is, in Maria's words: an online mirror of her
grandfather's catalogue so he could keep adding books, prices (several per
book) and edits. The transformation from Word to database was a one-time
migration. It ran twice: first on two non-identical versions of the
catalogue that had to be collated, then, after a months-long break, as a
full reimport of a single corrected version marked up with `! ` (edited)
and `AUS! ` (removed). The second run needed a separate database branch
because the first version was already deployed and in use.

So the portfolio does NOT present a "repeatable pipeline". It presents a
**migration done carefully, twice, with the evidence of why twice.** The
proof is traceability, not reruns: one book can be followed from its Word
row through `composite_id` to its database row, and every stage's code,
counts and logs are shown as they actually ran.

Chosen direction: curated real repo + case-study README + the migration
code restored as a readable archive + the existing Vercel deployment as the
live demo (bugs fixed). Splink is a later optional block. No separate
portfolio frontend. Frontend is shown as delivery, not as the selling point.

Constraints: book data and prices may be public; guests stay read-only;
limited time and energy; nothing deleted without her say; one step per
fresh session; she runs the dev server and deploys herself; every fix
that touches something she has not worked with (auth, middleware) gets a
one-line mechanism explanation before it is applied.

Every step ends with a hard stop.

## Immediate action on approval (this session only)

Copy this file to `docs/PORTFOLIO_PLAN.md` in the repo (creating `docs/`).
Nothing else is written, moved, or deleted this session. Steps 0–7 each
get their own fresh session.

## Step 0 — Secrets and the production switch (her actions, 15 min)

- Rotate the Neon password that sits in plain text in a commented
  `pg_dump` line in `.env`. Delete that line.
- Check the Vercel env: `NEXT_PUBLIC_DEV_MODE` must be absent or `false`.
  Mechanism: `frontend/src/lib/auth.ts` returns "allowed" for every
  permission check when that variable is `true`, so if it were set on
  Vercel, guests could edit.
- Both `.env` files were never committed; git is unaffected.

HARD STOP: confirm done before anything is pushed publicly.

## DONE! Step 1 — Frontend bug fixes (1 session, necessary)

Files: `frontend/src/lib/queries/books.ts`, `frontend/src/proxy.ts`,
`frontend/src/lib/auth.ts`, possibly one Alembic migration.

1. Pagination: add `ORDER BY` to the three list queries so pages are
   stable. Mechanism: without it PostgreSQL may return rows in a different
   order per query, so page 2 can repeat page 1.
2. Search: first ask Maria what search should match (whole original entry
   vs title/author fields), then fix accordingly and test her three
   symptoms: two-word names, Enter key, reload. If original entry: new
   trigram index on `book_admin.original_entry`.
3. `proxy.ts`: add `PATCH` to the guarded methods. Mechanism: soft-delete
   goes through `PATCH`, which the role check does not cover, so any
   logged-in viewer can mark books removed.
4. `auth.ts`: dev-mode bypass only when `NODE_ENV !== 'production'`.

Verification with the browser tools once she has started the dev server.

HARD STOP: she deploys, we check the live app.

## DONE! Step 2 — Tidy the tree, nothing deleted (1 session)

Every move is `git mv` into `archive/` unless she says delete.

- Untrack `.agents/skills/`, `.claude/skills/`, `skills-lock.json`,
  `*.DS_Store`; add to `.gitignore`; drop the stale
  `database/in_progress/*` lines.
- Move to `archive/`: `api/*_old.py`, `alembic/old/`, `page_old.tsx`
  files, `BookFormOld.tsx`, `database/tables/`, `database/reload/dev/`,
  `blavatsky.json`, `main.py`, `which_db.py`, `PROJECT_LOG.md` (January
  draft), `frontend/API_REFERENCE.md`, `frontend/CLAUDE_DESIGN_BRIEF.md`.
- Replace `frontend/README.md` boilerplate with five lines.
- Remove the commented-out SQL in `books.ts` and Mantine markup in pages.
- Second `venv/`: propose deletion, her call.

HARD STOP: she reviews the move list before any `git mv`.

## DONE! Step 3 — The migration as a readable archive (1–2 sessions)

Create `migration/` in the repo. Not a package, not runnable end to end,
no path fixes beyond what is needed to read it. Two iterations, shown as
they were, restored from git history and the backup folder:

```
migration/
  README.md                what happened, in order, with dates and counts
  iteration-1_2025-09/     two-version collation
    01_extract_and_collate/   data_prep_old.py (kp authoritative, p prices only)
    02_resolve_discrepancies/ resolve_discrepancies.py (95 / 75 thresholds)
    03_parse/                 parse_single_batch_old.py, batch_processor, check_status
    04_rematch_updated_docs/  match_parsed_entries.py (topic_changed, price_changed)
    05_people/                normalise_people.py, people_pass1/2, match_people2people.py
    06_validate/              validate_data4loading.py
    07_load/                  initial_load/* and the Alembic data migrations
    logs/                     processing_log, validation_log, discrepancy counts
  iteration-2_2026-05/     full reimport of one corrected version
    01_extract/               transform_docx.py (AUS! filter, ! marker, || joins)
    02_batch/                 data_prep.py (composite_id)
    03_parse/                 parse_single_batch.py (flag prompt), check_status.py
    04_people/                clean / nopes passes
    05_prepare/               prep_parsed.py
    06_load/                  database/reload/load_*.py, on a DB branch
    logs/                     book_counts_comparison.csv, loading logs
```

- Each stage folder gets a 5-line header file: input, output, what it
  decided, what it logged, what went wrong.
- Migrations: the four Alembic data migrations that import missing modules
  become no-op `upgrade()` with a docstring pointing at
  `migration/iteration-1/07_load`. The schema chain then builds an empty
  database with `alembic upgrade head`; that is about the schema, not
  about rerunning data.
- `database/connection.py`: replace bare `except:` with a printed error
  and re-raise.
- `load_b2p.py`: her call between a unique constraint or "run once" note.
- `requirements.txt` split into runtime and dev, plus a minimal
  `pyproject.toml`. No sample run, no CI.

HARD STOP: she confirms the two-iteration split and the folder names.

## DONE! Step 4 — One book, traced end to end (½ session)

Pick one real entry. Show, in `docs/trace.md`: the Word row (screenshot or
text), its raw JSON with price extracted, its `composite_id`, the parsed
JSON with flags, its `books2people` rows after dedup, its database row,
its page in the live app. This replaces the sample run: it proves the
pipeline on real data without pretending it is repeatable.

HARD STOP: she picks the book.

## Step 5 — README and docs (1–2 sessions, mostly writing)

- `README.md`: what it is, for whom, constraints, the two iterations and
  why, numbers table, three decisions and their cost, status with the real
  ending (delivered, in use, collection sold), how the app is run. Sources:
  `PROJECT_LOG_updated.md`, `beschreibung.md`, `/project` page.
  Include a "known limitations" section: the author filter needs 3
  letters, so two-letter surnames ("Ku") cannot be filtered; the full-text
  search is a substring match, so "Ku" also hits Kunst, Kultur, etc.
- `docs/data-quality.md`: the missing-books hunt (994 rows, set logic on
  composite ids, 122 cross-references) with the count table.
- `docs/entity-resolution.md`: two passes, surname blocking, nopes context
  pass, honest Splink paragraph with one chart.
- `docs/schema.md`: current tables one line each, the two schema changes
  and why, the database-branch approach for the reimport.
- Update `frontend/src/app/project/page.tsx` status text (both languages).

HARD STOP: she reads the README as a stranger would.

## Step 6 — Curate the notebooks (1 session)

`notebooks/` with five cleaned notebooks, each with a markdown header
(question, inputs, result): `get_the_numbers`; `08`+`09`+`10` merged;
`05`+`06` merged; `getting_fuzzy`+`refining_fuzzyness` merged; `16_0`
Splink labelled "unfinished experiment". The rest stays local/ignored.

HARD STOP: she approves the five before commit.

## Step 7 — Optional, later: finish Splink

Only after 0–6 and only if she wants it. Starting point: exact
`family_name` matches carry a negative weight in the saved waterfall
chart, so m/u estimation is wrong; her `support_notes.md` names the same
suspicion. Own review when she gets there.

## Verification of the whole plan

Fresh clone: README readable in five minutes; `migration/README.md` tells
the two-iteration story with counts; `docs/trace.md` follows one book;
`alembic upgrade head` builds an empty schema; live app search and paging
behave; guests cannot write.

## Deferred, deliberately

Worth doing eventually, but not part of getting the project
portfolio-ready, and not where her focus is:

- Remove or disable the signup route. It exists so potential buyers could
  log in and download lists; that never happened and the collection is
  sold. Noted 2026-09-15 while tidying the tree.
- Upgrade `nodemailer` past the four open advisories. The fix is
  `nodemailer@10`, a breaking change that also touches `next-auth`'s own
  pinned range. Two of the four advisories (RFC 5322 comment mis-parsing,
  addressparser DoS) are reachable through the signup address, so removing
  signup settles this one too.

## Out of scope, deliberately

Separate portfolio frontend. Making the migration rerunnable. Sample runs.
CI. Frontend restyle, Mantine removal, font-size switch. Rewriting any
pipeline logic.
