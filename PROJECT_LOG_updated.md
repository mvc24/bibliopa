# Bibliopa — Development Log

Digitising my grandfather's book bibliography: ~12,500 entries spread over
about 50 Word documents, turned into structured data, loaded into PostgreSQL,
and made searchable through a web app he uses himself.

**Live**: https://bibliopa.vercel.app
**End user**: my grandfather, 90, low vision and a hand tremor. He browses,
searches, and adds entries.
**Team**: me, solo. Claude as teaching assistant and pair programmer.

---

## Where the project stands

| | |
|---|---|
| Books in the database | 10,919 |
| People in the database | 8,947 (from 17,722 raw person records) |
| Topics | 46 categories, from ~50 source documents |
| Pipeline | Done and run twice (initial load + full reload) |
| Frontend | Deployed and in use; styling and features still in progress |

> **On the counts**: the documents hold 12,614 rows, the parsed JSON 12,492.
> The 122-row difference is rows that only contain a cross-reference
> ("siehe Assmann," and similar) rather than an entry — they have no
> bibliographic content to parse.

---

## Stack

**Pipeline (Python)**: `anthropic`, `python-docx`, `rapidfuzz`, `ijson`,
`psycopg2`, `sqlalchemy`, `alembic`, `python-dotenv`, `rich`

**Database**: PostgreSQL, hosted on Neon

**Frontend**: Next.js 16, React 19, React Aria Components, Tailwind 4,
next-auth, `pg`, react-hook-form + zod, TanStack Query — deployed on Vercel

```
Word documents → price consolidation → Claude API parsing → validation
    → matching against fresh documents → people deduplication → PostgreSQL
    → Next.js app
```

---

## Phase 1 — Schema design

**The question**: what shape should a bibliographic entry have?

I looked at existing cataloguing standards (MARC, Dublin Core) and found them
built for libraries with far more metadata than this collection has. I designed
a JSON schema instead, from the actual entries in the documents.

Decisions:

- **JSON, not a relational schema, for the parsing stage.** Parsing output is
  messy and the shape kept changing; a rigid schema would have meant a migration
  every time I learned something new about the data.
- **Nested person objects** for authors, editors, contributors, translators.
- **Multivolume support** as a nested list, because a lot of the collection is
  collected works and series.
- **Administrative block** on every entry to record how confident the parse was
  and whether it needs review.

```json
{
    "authors": [{"family_name": "string", "given_names": "string"}],
    "is_multivolume": "boolean",
    "volumes": [{"volume_number": "integer", "volume_title": "string"}],
    "administrative": {
        "parsing_confidence": "high|medium|low",
        "needs_review": "boolean"
    }
}
```

**What I learned**: reading a standard is worth it even when you don't adopt it —
MARC is where the author/editor/contributor distinction came from.

---

## Phase 2 — Understanding the source data

About 50 Word documents, each one topic, written over decades with no consistent
formatting.

I wrote a script to count entries per document and compare the two versions of
the bibliography (with prices, without prices) against each other.

What the counts showed:

- Sizes range from 20 entries (ZEITSCHRIFTEN) to 950 (FREMDSPRACHIGE LITERATUR
  IN ÜBERSETZUNGEN)
- The two versions disagree — entries had been moved, edited, deleted
- Prices appear in some documents and not others

**What I learned**: counting first was the right call. The counts are what later
made it possible to tell "the parser dropped an entry" apart from "the entry was
never there."

---

## Phase 3 — Parsing prototype with the Claude API

**The problem**: entries are free-form German text. Turning them into structured
fields by hand is not possible at this volume, and regex breaks on the third
entry.

I used the `anthropic` package with a prompt containing the schema, and tested
on samples picked for being awkward.

Two cases that shaped the prompt:

**A six-volume work**

```
CHURCHILL, Winston C. Der Zweite Weltkrieg. Memoiren.
1. Band Der Sturm zieht auf... [6 volumes]
```

Parsed into one work with six volume records, each with its own title, page
count, and illustration note.

**No author, several editors**

```
EIN GOTT DER KEINER WAR... Mit einem Vorwort von Richard Crossman
```

Parsed with an empty author list, Crossman and Borkenau as editors, and Koestler,
Gide, Silone as contributors — the distinction I'd taken from MARC in Phase 1.

**What I learned**: the schema does most of the work in the prompt. Describing
the desired output structure precisely mattered more than instructions about how
to behave.

---

## Phase 4 — Consolidating the two document versions

**The problem**: two versions of the bibliography existed. The "keine Preise"
(kp) version was current — my grandfather's latest edits. The "Preise" (p)
version was older but held the price information.

**The rule I set** (and this is the thing that made it tractable):

- **kp is the source of truth** for all bibliographic content and structure
- **p is a source for prices only**
- Where an entry in kp has an exact match in p, take the price; otherwise leave
  it empty and log the miss

Everything else followed from that. Without a stated rule, every mismatch is a
judgement call and there were hundreds of them.

**Implementation**: text normalisation, then exact matching, then fallback
search patterns for near-misses, with every unmatched entry written to a
discrepancy log.

```
Files processed:        16 (the two smallest size groups)
Entries consolidated:   1,086
Average match rate:     89%
Discrepancies logged:   72
```

**What I learned**: deciding which source wins, before writing any matching
code, is what turns an unbounded problem into a bounded one. Also: log what
didn't match. The discrepancy file was more useful than the success count.

---

## Phase 5 — Parsing everything

Scaling the Phase 3 prototype up to the whole bibliography, using the Claude
Batch API.

**Batching**: 25 entries per batch, each batch tracked with its own metadata:

```python
{
  "batch_id": "msgbatch_01ABC123...",
  "topic": "normalized_topic_name",
  "submitted_at": "timestamp",
  "entry_count": 25,
  "status": "completed"
}
```

**Composite IDs**: every entry got a `composite_id` of `topic_entry_batch`, so
any structured record could be traced back to the document line it came from.
This turned out to matter far more than expected — it's the key everything else
was later matched on.

**Cost**: about $200 for the full parse.

Scripts: `api/batch_processor.py`, `api/parse_single_batch.py`,
`api/check_status.py`.

**What I learned**:

- Batch submission is asynchronous; I needed a status-checking script and a
  place to record what had been submitted, or I'd have lost track of which
  batches had come back.
- Choosing an identifier scheme early paid off repeatedly.

---

## Phase 6 — Matching parsed data back to updated documents

**The problem**: my grandfather handed over updated documents after the parsing
was already done and paid for. Entries had moved between topics, titles had been
edited, some entries were gone and new ones added.

Re-parsing would have cost another $200. So instead: match the existing parsed
JSON against the new documents and keep the structured data.

**Approach**:

1. Match within topic first
2. Fall back to fuzzy text matching with RapidFuzz for edited entries
3. Score each match so uncertain ones can be reviewed
4. Validate before loading anything

```python
# matched output
{
  "composite_id": "new_topic_index",   # updated to the new location
  "title": "kept from the API parse",
  # ...all structured fields kept
  "admin": {
    "topic_changed": true,             # entry moved between topics
    "original_entry": "current raw text"
  }
}
```

**Validation before loading**: duplicate `composite_id`s across files, books
referencing people that don't exist, entries missing required fields.

```
Entries matched:      the full set
Match rate:           ~95% automatic
Flagged for review:   ~200 (missing titles and similar)
Topic moves:          hundreds
```

**What I learned**:

- When an external API result is expensive, treat it as an asset to be preserved
  rather than a step to be re-run.
- Pre-load validation catches things that are painful to untangle once they're
  rows in a table with foreign keys pointing at them.

---

## Phase 7 — Deduplicating people

**The problem**: 17,722 person records, with the same person appearing under
several spellings. "ADORNO, Theodor W.", "ADORNO, Th. W." and "Adorno, Theodor
W." were three unrelated records. Author search was therefore incomplete.

**Two passes, because there were two different problems.**

**Pass 1 — splitting records that hold more than one person**

```python
# in
{"display_name": "Otto Abel u. Wilhelm Wattenbach", "family_name": null}

# out
[
  {"display_name": "ABEL, Otto",         "family_name": "Abel",       "sort_order": 0},
  {"display_name": "WATTENBACH, Wilhelm","family_name": "Wattenbach", "sort_order": 1}
]
```

64 records needed splitting, across 3 batches.

**Pass 2 — linking spellings with a `unified_id`**

```python
# in
[{"display_name": "ADORNO, Theodor W."},
 {"display_name": "ADORNO, Th. W."},
 {"display_name": "Adorno, Theodor W."}]

# out — same unified_id, original spelling kept
[{"display_name": "ADORNO, Theodor W.", "unified_id": "adorno_theodor_w"},
 {"display_name": "ADORNO, Th. W.",     "unified_id": "adorno_theodor_w"},
 {"display_name": "Adorno, Theodor W.", "unified_id": "adorno_theodor_w"}]
```

Batched **by surname**, 251 batches, so each request saw all the candidate
variants of the same name together. Uncertain cases got `unified_id: "oops"`
for manual review — under 1%.

```
Person records in:     17,722
Deduplication batches: 251
Cost:                  ~$6
Runtime:               ~3h45
```

**What I learned**:

- Splitting one transformation into two passes was what made each pass simple
  enough to check. Trying to split and deduplicate in one prompt produced
  results I couldn't verify.
- How records are grouped into batches changes the output quality. Grouping by
  surname is the whole reason the deduplication worked.
- `display_name` and `unified_id` do different jobs: one preserves what he
  wrote, the other makes search work. Keeping both meant not having to choose.

Scripts: `api/people_pass1_batches.py`, `api/people_pass2_batches.py`,
`api/people_batch_processor.py`, `api/people_clean_prep.py`,
`api/people_nopes_prep.py`, `api/people_nopes_reattach.py`.

---

## Phase 8 — Database schema and loading

**The problem**: nested JSON with embedded authors, volumes and admin data had
to become normalised tables.

**First attempt — an orchestrator script**

```
db_orchestrator.py
  └── load_topics.py
  └── load_books.py
  └── load_people.py
  └── load_admin.py
```

It failed on partial runs: if books loaded and people didn't, there was no way
back except dropping everything by hand, and no record of what state the
database was actually in.

**What replaced it — Alembic migrations**

```
alembic/versions/
  ├── 2b89618ef060_rebuild_database_with_new_schema.py
  ├── c965577521b1_load_topics.py
  ├── a5ab158c3eb5_load_books.py
  ├── 382c5a14404f_load_people.py
  └── c25dfe60be3b_load_related_tables_data.py
```

Reasons: each migration is one transaction, so a failure rolls back instead of
leaving half a database; `alembic downgrade` undoes a step; `alembic upgrade
head` rebuilds from nothing; and the schema history lives in git.

**Tables**

```sql
books           -- book_id, composite_id (unique), title, subtitle, publisher,
                --   place_of_publication, publication_year, is_multivolume, ...
people          -- person_id, unified_id (unique), display_name, family_name,
                --   given_names, ...
books2people    -- book_id, unified_id, display_name, is_author, is_editor,
                --   is_contributor, is_translator, sort_order
book_admin      -- book_id, original_entry, + quality flags
prices          -- price_id, book_id, amount, imported_price
books2volumes   -- volume_id, book_id, volume_number, volume_title, pages, notes
topics          -- topic_id, topic_name, topic_name_german, entry_count
```

**The foreign key problem**: the JSON files have `composite_id`s, not database
IDs, and database IDs don't exist until the rows are inserted. Solved in two
stages — load books, then read the assigned IDs back out:

```python
book_ids = get_all_book_ids()          # SELECT composite_id, book_id
id_dict = {composite_id: book_id for composite_id, book_id in book_ids}

for entry in admin_data:
    entry["book_id"] = id_dict[entry["composite_id"]]
```

**Load order matters**: topics → books → people → related tables. Getting this
wrong produces foreign key errors that read as data problems but aren't.

**Deliberate denormalisation**: `books2people` keeps `unified_id` as text rather
than a foreign key to `people.person_id`, because the people table was still
changing. Flexible during development, to be tightened later.

```
Load time (full rebuild):  2–3 minutes
Rollback:                  tested, repeatedly
```

**What I learned**:

- Migrations over scripts, for anything that touches a database I care about.
  The deciding factor was rollback, not tidiness.
- Bulk inserts, never row-by-row. `op.bulk_insert()` with batching for the large
  tables.
- Keeping data-preparation code in Python modules and out of the migration
  files means the preparation can be run and checked on its own.

---

## Phase 9 — The reload

**The problem**: another round of updated documents, and by then I also knew the
first schema had things wrong in it. Rather than patch, I reloaded from source.

`data_reload/` holds the whole run: the original `.docx` files, `data_prep.py`,
the prepped intermediate files, and the final `db_files/` — `books.json`,
`people.json`, `books2people.json`, `book_admin.json`, `prices.json`,
`books2volumes.json`.

**Counts, checked per topic** (`book_counts_comparison.csv`):

```
Rows in the documents:   12,614
Records in the JSON:     12,492
Difference:                 122
```

Per-topic differences ranged from 0 (many topics matched exactly) to 14
(FRÜHES CHRISTENTUM, RELIGION ALLGEMEIN). The difference is rows that hold only
a cross-reference — "siehe Assmann," and similar — with no bibliographic content
to parse, so they produce no record.

**Schema changes made during the reload** (recorded in
`frontend/SCHEMA_CHANGES_AFTER_RELOAD.md`):

- `books`: `isbn` removed, `is_active` added
- `people` and `books2people`: `name_prefix`, `name_suffix` added
- `book_admin`: quality flags replaced entirely — out went
  `parsing_confidence`, `needs_review`, `topic_changed`, `price_changed`,
  `batch_id`; in came `corrected_by_api`, `missing_person`,
  `multiple_editions`, `api_concerned`, `problematic_multi_volume`
- `people_variants`: added for the reload, then dropped again once it had
  served its purpose

**Topics were never truncated.** Topic IDs had been remapped by hand once
already; that work is not repeatable cheaply, so the reload was built around
leaving the topics table alone.

**The missing books2people rows.** After reloading people and books2people, rows
were missing — books whose person links hadn't come across. Finding them took
several passes, and `data_reload/fix_missing/` is the record of it:
`b2p_list.json` → `b2p_found_list_01.json` → `b2p_found_data_02.json` →
`b2p_loading_file_01.json`. Commits: "working on fixing missing b2p rows",
"continue searching for b2p links", "work on matching missing people",
"loaded more b2p data".

**The German collation.** `family_name` and the other sortable text columns
carry `pg_catalog."de-x-icu"`, so that ä sorts with a and not after z. It was
lost during the reload and had to be re-added — twice
(`6d4a826e1f97`, `b3f7d2c1a890`). Without it, alphabetical browsing is wrong in
a way that is immediately visible to a German reader.

**Other migrations from this period**:

- `50f3cb025763` — `is_removed` on books (soft delete, nothing is ever deleted)
- `2f41dc3393f9` — `topic_normalised`, URL slugs for topics
- `da311bdcaadf` — trigram indexes for search
- `6ef7244b42c7`, `dd57c5529964`, `0e353367b092` — foreign key and visibility
  indexes, after list queries got slow
- `75a6066945d6` — topic name corrections

**What I learned**:

- Counting per topic, not just in total, is what made the missing rows findable.
- Collation is not cosmetic. It's part of the schema and it does not survive a
  reload on its own.
- A join table can load "successfully" and still be incomplete. The row count
  is the check, not the absence of errors.

---

## Phase 10 — The web app

Next.js App Router, talking to PostgreSQL directly through `pg` — no ORM on the
frontend side, queries written as SQL in `src/lib/queries/`.

**Structure**

```
src/app/
  page.tsx                       home
  books/[topic]/page.tsx         catalogue list for a topic (or /books/all)
  books/[topic]/[id]/page.tsx    book detail
  books/new/page.tsx             add a book
  people/[id]/edit/page.tsx      edit a person
  login, account, contact, project
  api/books, api/books/[id], api/people, api/authors,
  api/topics, api/prices, api/suggestions, api/auth
src/lib/
  db.ts          connection pool + query helper
  queries/       all SQL, one file per area
  auth.ts        session + role checks
```

**Access control**: next-auth with roles — admin, family, researcher, viewer,
and guests with no login. `hasPermission()` maps a role to actions (view, add,
edit, delete, view_prices, view_debug_info). `src/proxy.ts` enforces it at the
route level before a page renders.

**Soft delete**: `markBookAsRemoved()` sets `is_removed`; nothing is deleted.
Removed books stay retrievable through `getAllRemovedBooks()`.

**Things that came up**:

- **Turbopack runs out of memory on this machine.** Dev runs with
  `next dev --webpack`; the flag is `--webpack`, not `--no-turbopack`.
- **Slow list queries** — fixed by adding the foreign key indexes above, after
  looking at where the time actually went.
- **Search** currently runs `ILIKE` against `book_admin.original_entry`, which
  searches the entire original text of an entry. Trigram indexes exist. Known
  limitation: names of two letters can't be searched ("Ku, Hung Ming").

---

## Phase 11 — Redesign: Mantine → React Aria

**Why**: Mantine's styling was hard to override, and the accessibility
requirements here are specific and non-negotiable. React Aria Components ship
unstyled and accessible, which is the right way round for this.

**The requirements**, written down first as a design brief
(`frontend/CLAUDE_DESIGN_BRIEF.md`):

- Body text contrast ≥ 7:1 (WCAG AAA), never below 4.5:1
- Borders, icons, focus rings ≥ 3:1
- Base font size ≥ 18px, holding up at 21px and 24px
- Interactive targets ≥ 44×44px, because of the tremor
- Always-visible focus indicator, ≥ 2px with offset
- No state shown by colour alone — always weight, border, underline or icon too

**Styling approach**: classless. Components carry no utility strings; all CSS
lives in `globals.css`, keyed on design tokens in `:root` and the
`react-aria-*` default classes. Changing the look means editing one file.

**Component mapping**

| Mantine | React Aria / HTML |
|---|---|
| TextInput / Textarea | `TextField` → `Label` + `Input` / `TextArea` |
| NumberInput | `NumberField` |
| Select (fixed options) | `ComboBoxField` |
| Autocomplete (free text) | `ComboBoxField` + `allowsCustomValue` |
| Chip.Group (multi-select) | `ToggleButtonGroup` — large targets, for the tremor |
| Modal | `Modal` + `Dialog` |
| Table (list) | `GridList` + `GridListItem` |
| Table (key/value detail) | `<dl>` description list |
| Pagination | custom prev / next |

**Shared components built**: `ComboBoxField` (Enter-to-select when one match
remains, clearable, configurable menu trigger), `SearchBox`, `AuthorFilter`
(matches on surname behind a 3-character gate), `PriceDialog`.

**Things learned about RAC**:

- Unstyled means overlays are genuinely invisible without positioning CSS, and
  checkbox boxes and listbox highlights have to be drawn.
- For a custom ComboBox filter, omit `defaultFilter` and control `items`
  directly.
- `GridListItem href` makes the whole row a real link, so open-in-new-tab works.

**Still open**: a handful of pages still import Mantine (account, contact,
project, login, home, books/new). `MantineProvider` in `providers.tsx` comes out
last, then Mantine can be uninstalled. The font-size switch (Normal / Large /
Larger, scaling the root rem) is designed and tokenised but not built.

---

## Phase 12 — Deployment

Vercel for the app, Neon for PostgreSQL.

Adjustments this required:

- **Connection pool `max: 1`.** Serverless functions each open their own pool;
  a normal pool size multiplied by the number of concurrent functions exhausts
  the database connection limit.
- **`connectionTimeoutMillis: 10000`**, up from the default — cold connections
  to Neon are slower.
- **`ssl: { rejectUnauthorized: false }`**, required for Neon.
- **Static files excluded from the auth middleware**, or the logo doesn't load
  on the login page (commit b50e808).

---

## In progress

**User accounts** (uncommitted). Invite-based: an account is created inactive,
the user gets a signed link, sets their own password, and the account activates.

Tokens are HMAC-signed and stored nowhere (`src/lib/tokens.ts`). The signing key
is `NEXTAUTH_SECRET` plus a binding value taken from the user's own row, so a
link dies when that value changes:

- set-password links bind to `password_hash` → single use
- verify-email links bind to `is_active` → dead once activated

Email through Resend. Query functions added: `getUserByEmail`, `getUserById`,
`createUser`, `setPassword`, `activateUser`.

**Known issues** (`todos.md`):

- Two-letter names can't be searched ("Ku, Hung Ming")
- Number of copies: not editable, not displayed
- Topic not shown on the overview page
- No way to search by price

**Frontend, still to do**: finish removing Mantine, build the font-size switch,
overview page header and search toolbar layout, topic chips on catalogue cards.

---

## What this project taught me

**On data**

- Decide which source is authoritative before writing matching code. Every
  ambiguous case then has an answer already.
- Count things per group, not just in total. Totals hide exactly the problems
  you're looking for.
- Log what didn't match. The failures are more informative than the successes.
- Choose an identifier scheme early and keep it stable — `composite_id` is what
  made re-matching and reloading possible at all.

**On the API**

- The schema does most of the work in a parsing prompt.
- How records are grouped into batches changes the output. Grouping people by
  surname is why the deduplication worked.
- Splitting a hard transformation into two simple passes made both checkable.
- $206 in API calls against months of manual work was not a close call.

**On the database**

- Migrations over scripts, for rollback more than for tidiness.
- Bulk inserts, always.
- Collation is part of the schema and doesn't survive a reload by itself.
- A join table can load without errors and still be missing rows.

**On the frontend**

- Accessibility requirements written down as numbers before any design work
  meant every later decision had something to check against.
- Unstyled components plus central CSS turned out to be less work than fighting
  a component library's styling.

**On working this way**

- Fresh conversation per phase. Long ones drift.
- Pseudocode first, then code.
- Nothing gets deleted — soft deletes in the database, old components kept as
  `*Old.tsx` files.

---

*Log covering the project from the first schema sketch through the deployed app.*
