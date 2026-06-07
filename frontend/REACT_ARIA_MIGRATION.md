# React Aria migration — handoff

Migrating from Mantine → React Aria Components (RAC) + Tailwind. Mantine and RAC
coexist during the migration. Styling is **classless**: components carry no
utility strings; all styling is central in `src/app/globals.css`, against the
design tokens in `:root` + the `react-aria-*` default classes and our semantic
hooks.

**Why:** Mantine styling is hard to override; RAC is unstyled so we get full
control. Accessibility is the priority (low vision + hand tremor: large text,
large targets, keyboard nav, visible focus, Enter-to-select).

---

## Done

**Shared components** (`src/components/elements/`)
- **`ComboBoxField`** — the reusable combobox. Enter-to-select when one match
  remains, optional `isClearable` ×, per-field `menuTrigger` (`focus` for short
  fixed lists, `input` for long/fetched). Uses non-deprecated `value`/`onChange`.
- **`SearchBox`** — RAC `SearchField`; calls `onSearch` on Enter + clear button.
- **`AuthorFilter`** — RAC `ComboBox`, matches on surname, 3-character gate,
  navigates to the author. Scoped to authors by the `/api/authors` query.
- **`PriceDialog`** — shared RAC modal for adding a price (list + detail).

**Pages / nav**
- **Nav** (`AppShell`, `MainNav`, `TopicsNav`) — off Mantine, classless. Top bar
  + collapsible topic sidebar; avatar menu = RAC `Menu`.
- **Bibliography list** (`books/[topic]`) — catalogue is a RAC `GridList` (rows
  are links → open-in-new-tab works); custom prev/next pagination; price modal.
- **Detail** (`books/[topic]/[id]`) — vertical Mantine table → semantic `<dl>`
  description list; shared `PriceDialog`; remove / edit / price wired.
- **`BookForm`** — fully migrated + styled. `FormEvent`→`SyntheticEvent`;
  `formatExtras` → `ToggleButtonGroup`; custom checkbox indicator removed (box
  drawn in CSS); all placeholder utility classes stripped.

**Styling**
- `globals.css` — design tokens (palette, Jenson Pro serif + Zeitung sans, type
  scale, spacing, sizing) in `:root`; central CSS for nav, catalogue, detail,
  form controls, modal, pagination, and action chips. Fonts via Typekit `@import`.

### Component mapping used
| Mantine | React Aria / HTML |
|---|---|
| TextInput / Textarea | `TextField` → `Label` + `Input` / `TextArea` |
| NumberInput | `NumberField` (empty = `NaN`) |
| Select (enforced) | `ComboBoxField` (`value` / `onChange`) |
| Autocomplete (free text) | `ComboBoxField` + `allowsCustomValue` |
| Chip.Group (multi-select) | `ToggleButtonGroup` + `ToggleButton` (tremor) |
| single Checkbox / Chip | classic `Checkbox` (box drawn in CSS) |
| Select → navigate | custom `AuthorFilter` |
| Menu | `MenuTrigger` + `Menu` + `MenuItem` + `Popover` |
| Modal | `Modal` + `Dialog` (controlled `isOpen`) |
| Table (list) | `GridList` + `GridListItem` |
| Table (detail key/value) | `<dl>` description list |
| Card / Stack / Group / Title / Text | `div` / `section` / `<h*>` / `<p>` + central CSS |
| Pagination | custom prev / next |
| Anchor / NavLink | next `Link` + `aria-current` |

---

## Still open

**Styling polish — toward the design mockup (needs component edits, not just CSS)**
- Overview page header: title + "Privatbibliographie · …" line + result count.
- Search toolbar layout + a prominent "+ Titel aufnehmen" CTA (currently
  "Katalogisieren" lives in the nav).
- Catalogue cards: topic chip + icons (tag / archive); dashed empty-price chip;
  label wording ("Als entfernt markieren" vs the code's "Abschreiben").
- Detail page: optional old-library-catalogue-card variant for the grandfather
  (A/B, shown manually — no infra needed). Low priority.
- **Font-size Switch** (Normal / Large / Larger, scales the root rem). Tokens ready.

**Remaining Mantine** (still coexisting; migrate, then drop Mantine)
- Pages: `account`, `contact`, `project` (mostly empty), `login` (one form),
  `people/[id]/edit` (not in use yet), `page.tsx` (home), `books/new`
  (Box/Stack/Title wrapper).
- `books/[topic]/page.tsx` — the search toolbar is still wrapped in Mantine
  `Card` / `Stack` / `Group`.
- `providers.tsx` — `MantineProvider` + `@mantine/core/styles.css`. **Remove
  LAST**, once nothing else imports Mantine; then uninstall Mantine and drop the
  Mantine type import + old `startsWithFilter` from `selectFilters.ts`.

**Deprecations**
- Classic `Checkbox` (8 in `BookForm`) is deprecated in RAC 1.18 →
  `CheckboxField` + `CheckboxButton`. **Kept on purpose:** CheckboxField forces
  an indicator back into the markup; we draw the box in CSS instead. Works fine;
  revisit only if RAC actually removes `Checkbox`. (`FormEvent` already fixed.)

**Optional / later**
- New-person role checkboxes are a multi-select → could become a
  `ToggleButtonGroup` (needs a small state reshape).
- Backups to delete when confident (your call, not mine): `BookFormOld.tsx`,
  `books/[topic]/page_old.tsx`, `books/[topic]/[id]/page_old.tsx`.
- Pre-existing: unused `topics` / `setTopics` state in `BookForm`.

---

## Verified facts (don't re-derive)
- `react-aria-components` **1.18.0**. Deprecated: classic `Checkbox` (→
  CheckboxField + CheckboxButton); ComboBox `selectedKey`/`onSelectionChange`
  (→ `value`/`onChange`); React `FormEvent` (→ `SyntheticEvent`).
- RAC ships **unstyled** — overlays (Modal/Popover) need positioning CSS or
  they're invisible; checkbox box and listbox highlight need CSS to show state.
- `ComboBox` custom filter: omit `defaultFilter` and control `items` yourself
  (AuthorFilter does this for the 3-char gate + surname match).
- `GridListItem href` makes the whole row a real link (new-tab); RAC uses the
  item `id` as the collection key, so the scroll-restoration DOM id sits on an
  inner `<div>`.
- Dev server: `npm run dev` (`--webpack`; Turbopack OOMs on this machine).
