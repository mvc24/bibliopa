# React Aria migration — handoff

Migrating form components from Mantine → React Aria Components (RAC) +
Tailwind. Mantine and RAC coexist during the migration.

**Why:** Mantine styling is hard to override; RAC is unstyled so Tailwind has
full control. Accessibility matters (end user has poor eyesight: large text,
keyboard nav, Enter-to-select in comboboxes).

---

## Done

- **`src/lib/selectFilters.ts`** — added `startsWithFilterRA(textValue, inputValue)`
  for RAC's `defaultFilter` (per-item, returns boolean). Old Mantine
  `startsWithFilter` left in place — `AuthorFilter` still uses it. Both reuse the
  shared `normalizeGerman` (umlaut folding).
- **`src/components/forms/BookForm.tsx`** — fully migrated to RAC. All form logic
  unchanged; only imports + JSX swapped. Typechecks clean.
- **`BookFormOld.tsx`** — untouched Mantine backup. Delete once confident.
- **Skill wired** — `.claude/skills/react-aria` symlink → `.agents/skills/react-aria`
  (loads as a proper skill from next session).
- **Tailwind IntelliSense** installed (clears the `@plugin` editor warning).

### Component mapping used

| Mantine | React Aria |
|---|---|
| `TextInput` | `TextField` → `Label` + `Input` |
| `NumberInput` | `NumberField` → `Label` + `Input` (empty = `NaN`) |
| `Select` (enforced list) | `ComboBox` (no `allowsCustomValue`) |
| `Autocomplete` (free text) | `ComboBox` + `allowsCustomValue` |
| `Checkbox` / `Chip` (toggle) | `Checkbox` (classic) |
| `Chip.Group` (multi) | `CheckboxGroup` + `Checkbox` |
| `Button` | `Button` (`onPress`, not `onClick`) |
| `Stack`/`Group`/`Divider`/`Text` | `div` + Tailwind / `<hr>` / `<span>` |

---

## To do

1. **Enter-to-select when one result remains** — NOT working yet. RAC ComboBox
   does not auto-highlight the first match, so currently it's ↓ then Enter. Need
   to find the right RAC mechanism (was mid-investigation in the docs/skill).
   This is a real accessibility requirement, not cosmetic.
2. **Styling pass** — the form is intentionally near-unstyled (looks bad on
   purpose). Approach:
   - Define design tokens (colours, font sizes, font family) in
     `src/app/globals.css` under `@theme inline` (already has
     `--color-background`, `--color-foreground`, fonts).
   - Then style RAC components. With the
     `tailwindcss-react-aria-components` plugin (already in globals.css line 2),
     use named state variants: `selected:`, `focused:`, `hovered:`, `pressed:`,
     `disabled:` etc. — no `data-[...]` prefix needed for an element's own state.
   - VERIFY: whether parent-state targeting shortens from `group-data-[selected]:`
     to `group-selected:`.
   - The current placeholder classes to replace: `border`, `bg-background`,
     `px-2 py-1`, and the `CheckboxBox` `✓` indicator.
3. **Other components still on Mantine** — `AuthorFilter.tsx` and anything else
   importing `@mantine/*`. Migrate, then remove Mantine deps.
4. **Pre-existing**: unused `topics`/`setTopics` state in BookForm (was there
   before; topic list comes from the `TOPICS` constant).

---

## Verified facts (don't re-derive)

- `react-aria-components` **1.18.0** exports BOTH `Checkbox` (classic) and
  `CheckboxField`/`CheckboxButton` (newer). We used classic `Checkbox`.
- RAC ComboBox `defaultFilter` signature: `(textValue, inputValue) => boolean`.
- The skill docs (`.agents/skills/react-aria`) show some **newer v2-style** API
  (subpath imports, `CheckboxField`); 1.18.0 supports both, but prefer the
  classic single-component forms for less markup.
- Dev server: `npm run dev` (uses `--webpack`; this machine OOMs with Turbopack).

## Files touched
- `src/lib/selectFilters.ts`
- `src/components/forms/BookForm.tsx`
- `.claude/skills/react-aria` (symlink, new)
