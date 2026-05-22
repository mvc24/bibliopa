# Frontend Schema Changes After Reload

Notes on what needs updating in the frontend once the production database has been reloaded with the new schema. Based on the schema diff between old production and the reloaded dev database.

Everything below assumes you are working on a separate git branch for the frontend changes.

---

## Database changes that affect the frontend

### `books` table
- **`isbn` column removed.** Any reference to it must go.
- **`is_active` column added** (integer).

### `people` table
- **`name_prefix` column added.**
- **`name_suffix` column added.**

### `books2people` table
- **`name_prefix` column added.**
- **`name_suffix` column added.**

### `book_admin` table — fully replaced
- **Removed:** `parsing_confidence`, `needs_review`, `topic_changed`, `price_changed`, `batch_id`
- **Added:** `corrected_by_api`, `missing_person`, `multiple_editions`, `api_concerned`, `problematic_multi_volume`

### `people` table — collation
- The German collation on `family_name` (`pg_catalog."de-x-icu"`) was lost in dev and needs to be re-added before or during production reload. Affects sort order on lists.

### `people_variants` table
- Removed entirely. Was only used during the reload — disregard for frontend.

---

## Places to update in `frontend/src/types/database.ts`

### `Book` interface (line 26)
- Line 36: remove `isbn?: string | null`
- Add `is_active: boolean` (or `number`, depending on how it's used — column is `integer` in the schema)

### `Person` interface (line 76)
- Add `name_prefix?: string | null`
- Add `name_suffix?: string | null`

### `Books2People` interface (line 88)
- Add `name_prefix?: string | null`
- Add `name_suffix?: string | null`

### `BookAdmin` interface (line 160)
Replace the field list:
- Remove: `parsing_confidence`, `needs_review`, `topic_changed`, `price_changed`, `batch_id`
- Add: `corrected_by_api`, `missing_person`, `multiple_editions`, `api_concerned`, `problematic_multi_volume` (all boolean)

### `BookOverviewWithAdmin` (line 66)
- Uses `topic_changed` — needs to be replaced with whichever new flag(s) take its place in the UI.

### `BookDetail.admin_data` (line 311)
- Uses `topic_changed`, commented-out `needs_review` and `parsing_confidence` — same as above.

### `BookDisplayRow` (line 320)
- Uses `parsing_confidence`, `needs_review`, `topic_changed`, `price_changed`, `batch_id` — needs full rewrite for the new admin columns.

### `CreateBookInput` (line 201)
- Line 209: remove `isbn?: string`

### `CreatePersonInput` (line 232)
- Add `name_prefix?: string` and `name_suffix?: string` if forms should allow setting them.

---

## Not checked / open questions

- Fields in the frontend types like `illustrations`, `packaging`, `topic_id`, `is_translation`, `original_language` weren't visible on the dev side of the schema diff. The diff might just hide unchanged context. Verify these columns still exist in the reloaded production before assuming the types are correct.
- The "stupidly complicated & unused types" section starting at line 269 is already flagged as junk — clean up scope is open.

---

## Beyond the types file

The types file is just the contract. After updating it, the actual breakage happens in:
- API route handlers (anywhere that runs SQL or builds objects matching these types)
- React components that read removed fields
- Forms that write removed fields
- Admin screens — these will need the most work because the `book_admin` columns changed completely

Use TypeScript errors as the worklist: once the types are updated, the compiler will point at every file that needs touching.
