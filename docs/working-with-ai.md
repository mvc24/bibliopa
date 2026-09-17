# Working with an LLM: in the pipeline, and as a tool

Two different things happened in this project under the name "AI", and
they should be judged separately.

1. **A language model is a component of the pipeline.** Every catalogue
   entry was parsed into JSON by Claude through the Batch API, and person
   records were deduplicated the same way. That is prompt design,
   output validation and cost control, and it is data engineering.
2. **A language model was my teacher and, for the web app, my pair
   programmer.** I learned Python on this project. How much I delegated,
   how I kept control of what was delegated, and where that went wrong,
   is the second half of this page.

---

## 1. The model inside the pipeline

### What it does

Each of the 12,492 entries is free-form German text like this:

```
KERTESZ, Imre/ ESTERHAZY, Peter/SCHULZE, Ingo. Eine, zwei, noch eine
Geschichte/n. Berlin Verlag 2008. 94 S. OPbd.
```

The model returns one JSON object per entry with about thirty fields:
title, people by role, place, publisher, year, pages, binding
abbreviation and its expansion, edition, condition, copies, translation
and multi-volume structure, plus an administrative block. The full system
prompt is in [`pipeline/iteration-2/03_parse/parse_single_batch.py`](../pipeline/iteration-2/03_parse/parse_single_batch.py).

### What changed between the two runs

Iteration 1 asked the model for a `parsing_confidence` of high, medium or
low and a `needs_review` boolean. After the run, neither was usable:
"medium" told me nothing about *what* to check, and the model set
`needs_review` inconsistently.

Iteration 2 replaced both with six boolean flags. Each flag has a
definition, examples taken from iteration-1 output, and a rule that
`verification_notes` must explain any flag that is set.

| Flag | Set when | What the model may do |
|---|---|---|
| `is_reference` | the row is a cross-reference ("Siehe …") | stop parsing, fill nothing else |
| `corrected_by_api` | an obvious typo with one plausible fix | apply the fix, record the reasoning |
| `missing_person` | a role is named but the name is absent | parse the rest, flag |
| `multiple_editions` | more than one edition or conflicting copy counts | first-described edition becomes the record, the rest goes in notes |
| `api_concerned` | world knowledge contradicts the entry | change nothing, flag |
| `problematic_multi_volume` | volume structure cannot be parsed cleanly | record only the clear volumes |

The rule that matters most is at the end of the prompt:

> When in doubt, prefer flagging over correcting. A flagged record can be
> reviewed; a wrongly-corrected record is invisible.

The examples were chosen from real output, including one where the
model's correction would have been wrong: it wanted to change
`MICHELAGNIOLO BUONAROTI` to "Michelangelo", but "Michelagniolo" is a
legitimate historical variant. The actual typo was the single R in the
surname. That case is in the prompt as a caution.

### What was kept out of the prompt

- **Prices.** In iteration 1 the price was sent with the entry and came
  back parsed. In iteration 2 it is extracted with a regular expression
  before batching and merged back afterwards by `custom_id`. The model
  never sees it.
- **Name splitting.** The model returns `display_name` as one string per
  person. Splitting into family name, given names and particles is a
  separate stage, because doing both in one prompt produced output that
  could not be checked.
- **Topic.** Sent as context, never returned; it comes from the filename.

### Checking the output

- Every batch file's input ids are compared with the output ids after
  retrieval. This is how the 1,008 entries the API silently dropped were
  found, though only in August 2026, three months after the run.
  See [`data-quality.md`](data-quality.md).
- Two rows came back with no title and were rejected by the `NOT NULL`
  constraint at load time.
- Flags and notes are stored in `book_admin`. Showing them on the book
  page for logged-in users, as a review queue, was planned and is not
  built; review currently means querying the table.

### Cost

| Run | Model | Entries | Cost |
|---|---|---|---|
| Iteration 1 parse | `claude-sonnet-4-20250514` | 12,573 | about 200 € |
| Iteration 1 people, two passes | same | 17,722 rows, 255 batches | about 6 € |
| Iteration 2 parse | `claude-sonnet-4-6`, prompt cached | 12,492 | not recorded separately; system prompt cached |
| Iteration 2 people, clean + nopes | same | 7,817 + 1,223 | 57 batches |

Batch API, temperature 0, one request per entry, 25 entries per file.

---

## 2. The model as a working tool

### What I delegated and what I did not

| Done by me, with the model explaining | Delegated to the model, reviewed by me |
|---|---|
| every pipeline script in `pipeline/` | most of the React components in `frontend/src/components/` |
| the collation rule (kp is truth, p is prices only) | TypeScript wiring between form, API route and query |
| `composite_id` and `unified_id` design | Alembic migration boilerplate |
| the six-flag design and the prompt text | CSS from a written design brief |
| all SQL in `frontend/src/lib/queries/` | the `README.md` files in `pipeline/` (from my notes and the git history) |
| people matching in the notebooks | this documentation, from my drafts |
| deciding what to load, when, onto which branch | |

The split follows interest. I wanted to understand the data work line by
line and I did not want to spend the same effort on the web app. Of 279
commits, 96 touch `frontend/`.

### How I kept control

Delegating to a model is only safe if the instructions are written down
and enforced. Mine evolved from a paragraph pasted into each chat to a
set of rule files the tool reads on every session. The rules that did the
most work:

- **Teach, do not solve.** For pipeline work the model was not allowed to
  write code; it explained the mechanism and I wrote it. This was the
  point of the project.
- **One step, then stop.** No plans for the next five steps, no "while
  we're here". A step ends with my decision, not the model's.
- **Ask when unsure; do not guess about my data.** The model does not
  know the shape of `people_sorted` or why `books2people` has a
  `composite_id` column. If it needs to know, it asks one question.
- **Use my names.** Variable names, table names, German labels are not to
  be "improved".
- **Never delete.** Old files are moved to `archive/`, not removed.
- **Fresh session per task.** Long conversations drift.

These rules live in `CLAUDE.md` at the repo root and in a per-project
memory the tool maintains between sessions. Every violation I caught
became a new line in that memory.

### Where it went wrong, and what I learned from it

Two failures are worth recording because they are the kind an employer
should ask about.

**The model wrote code I could not debug.** Early on, when I let it write
matching logic, the result used comprehensions and nested structures I
did not yet read fluently. It worked until it did not, and at that point
I had no way in. The fix was the "teach, do not solve" rule: slower, and
the only way the code stayed mine.

**The model reasoned in circles instead of asking.** During the Splink
work I asked how to interpret a chart. The model's reasoning trace ran to
dozens of paragraphs, repeatedly noting that it needed information about
my data and repeatedly not asking for it, then proposing a fix anyway. I
went through the trace line by line, marked every place it should have
stopped, and turned that into a rule: a sentence like "I should ask
before proposing" in the model's reasoning must end the turn with the
question. Reviewing a model's reasoning, not only its answer, is now part
of how I work with one.

### What I would tell someone starting the same way

- The model is good at syntax and bad at knowing what your data looks
  like. Keep the second part yours.
- Write the rules down and keep them under version control. A rule that
  lives in chat history is not a rule.
- Delegate what you do not need to own. Own everything you will have to
  debug at eleven at night.
