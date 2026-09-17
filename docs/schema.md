# Schema

PostgreSQL on Neon. The schema is built by `alembic upgrade head`
(24 migrations). The data migrations from iteration 1 are no-ops with a
pointer to `pipeline/iteration-1/07_load/`, so the chain builds an empty
database without the data files.

## Tables

| Table | One line |
|---|---|
| `topics` | 46 topics, `topic_normalised` is the URL slug; never truncated since the first load because ids were remapped by hand once |
| `books` | one row per catalogue entry; `book_id` serial, `composite_id` unique text from the pipeline, `is_active` integer for visibility levels, `is_removed` for soft delete |
| `book_admin` | one row per book: `original_entry` (the text as my grandfather wrote it), the five parser flags, `verification_notes` |
| `people` | one row per resolved person; `person_id` serial, `unified_id` unique text, name split into `family_name`, `given_names`, `name_prefix`, `name_particles`, `name_suffix`, `single_name`; `is_organisation` |
| `books2people` | one row per person per book with four role booleans (`is_author`, `is_editor`, `is_contributor`, `is_translator`) and `sort_order`; carries both `book_id`/`composite_id` and `person_id`/`unified_id` |
| `prices` | several per book; `imported_price` marks the ones from the documents, `source` and `date_added` for ones added in the app |
| `books2volumes` | volumes of multi-volume works: number, title, pages, notes |
| `users`, `sessions` | next-auth; roles admin, family, researcher, viewer |

Definitions as Python dicts: [`database/table_schemas.py`](../database/table_schemas.py).

## Two ids per record

`books` and `people` each carry a serial id and a text id. The serial id
is for joins and the app. The text id is for the pipeline: `composite_id`
encodes the topic and row position in the source document,
`unified_id` is a normalised name. `books2people` stores both pairs.

This is redundant on purpose. When the people table was accidentally
reloaded during iteration 1 and three sets of `person_id` values existed,
`unified_id` was what recovered the links. When the reload assigned new
`composite_id` values to 92% of books, `book_id` was what the app kept
working on.

## What changed between the iterations

| Change | Why |
|---|---|
| `books.isbn` removed | never going to be researched for a private collection |
| `books.is_active` added as integer, not boolean | so entries with certain parser flags can be held back from display, with room for levels (0 hidden, 1 visible, 2 visible but in a review queue) |
| `people.name_prefix`, `name_particles`, `name_suffix` split out | one field for all of them made sorting and conditional rendering impractical |
| `book_admin` flags replaced | out: `parsing_confidence`, `needs_review`, `topic_changed`, `price_changed`, `batch_id`; in: `corrected_by_api`, `missing_person`, `multiple_editions`, `api_concerned`, `problematic_multi_volume` |
| `people_variants` added, then dropped | held known spellings during the reload's matching step |
| German collation on sortable text columns | `pg_catalog."de-x-icu"` so ä sorts with a; lost in the reload and re-added twice (`6d4a826e1f97`, `b3f7d2c1a890`) |
| trigram indexes on `original_entry` | substring search in the app |
| foreign-key and visibility indexes | list queries were slow |

## The reload on a branch

The first version was live and in use when the reload happened. Neon
supports database branches, so the reload went onto a branch:

1. branch from production
2. truncate everything except `topics`
3. load books, people, related tables, `books2people` with `executemany`
   and `ON CONFLICT DO NOTHING`
4. reset each serial sequence to `MAX(id)` so rows added in the app do
   not collide
5. compare counts per topic against the documents
6. promote the branch

The load order matters: books first because they carry the ids, then
people, then the three related tables, then `books2people` last because
it references both.

## Known constraint gaps

- `books2people` has no unique constraint on `(book_id, person_id)`.
  20 rows violate the intended rule; the constraint waits for their merge.
- `books2people.unified_id` is text, not a foreign key to `people`, from
  when the people table was still changing.
