# RAC style inventory — tokens, components, states

Planning doc for the Mantine → React Aria Components (RAC) migration and the
global styling pass. Companion to `REACT_ARIA_MIGRATION.md`.

**Goal:** migrate every component **classless** (no Tailwind utility strings
baked into components — RAC emits default classes like `react-aria-Input`,
`react-aria-ListBoxItem`). All styling then lives centrally in
`globals.css` + tokens, so a restyle never reopens a component file.

**Highest priority is accessibility** — the end user has low vision and a
hand tremor. That drives the token targets below (contrast, font size,
visible focus, large target size).

---

## How styling attaches (the mechanism)

- Every RAC component renders a default class when no `className` is passed:
  `react-aria-Button`, `react-aria-Input`, `react-aria-ListBoxItem`, etc.
- Interactive state is exposed as attributes (`focused`, `selected`,
  `hovered`, `pressed`, `disabled`, `invalid`, …).
- With the `tailwindcss-react-aria-components` plugin (already in
  `globals.css`), those are state **variants** — `focused:`, `selected:`,
  `hovered:`, `pressed:`, `disabled:`, `invalid:` — **no `data-` prefix
  needed**. Parent-driven styling uses `group-*` or a render-prop.
- So: components stay classless; one central stylesheet targets the
  `react-aria-*` classes + state variants.

---

## 1. Tokens

Build on the existing `globals.css` tokens (`--color-background`,
`--color-foreground`, fonts). Add the rest. Targets are WCAG; aim AAA where
the eyesight benefits.

### Colour (semantic, not raw hues)

| Token | Role | Accessibility target |
|---|---|---|
| `--color-background` *(exists)* | page bg | — |
| `--color-foreground` *(exists)* | body text | ≥ 7:1 on background (AAA body) |
| `--color-surface` | cards, popovers, menus | — |
| `--color-surface-foreground` | text on surface | ≥ 7:1 on surface |
| `--color-border` | input/card borders, dividers | ≥ 3:1 vs adjacent (1.4.11) |
| `--color-primary` | primary action bg | — |
| `--color-on-primary` | text/icon on primary | ≥ 4.5:1 on primary |
| `--color-selected` | selected item / checked bg | ≥ 3:1 vs surface |
| `--color-on-selected` | text on selected | ≥ 4.5:1 on selected |
| `--color-hover` | subtle hover bg | distinguishable, not sole cue |
| `--color-muted-foreground` | secondary text | still ≥ 4.5:1 |
| `--color-focus-ring` | keyboard focus outline | ≥ 3:1 vs adjacent (2.4.11) |
| `--color-invalid` | error text/border | ≥ 4.5:1; never colour-only |
| `--color-disabled-foreground` | disabled text | exempt from contrast, keep legible |
| `--color-disabled-background` | disabled bg | — |

### Typography

| Token | Notes |
|---|---|
| `--font-sans` *(exists)* | body |
| `--text-base` | **large base for low vision — ≥ 18px** |
| `--text-sm` / `--text-lg` / `--text-xl` / `--text-2xl` | scale off base |
| `--font-weight-normal` / `--font-weight-medium` / `--font-weight-bold` | |
| `--leading-normal` / `--leading-tight` | line height |

### Sizing & shape

| Token | Role | Target |
|---|---|---|
| `--size-target-min` | min hit area for controls | **44px (tremor; WCAG 2.5.5 AAA)** |
| `--size-control-h` | input/button height | ≥ target-min |
| `--radius` | corner radius | — |
| `--border-width` | default border | ≥ 1px, 2px if it carries meaning |
| `--focus-ring-width` | outline thickness | ≥ 2px |
| `--focus-ring-offset` | gap to element | ≥ 2px |
| `--space-*` | padding / gaps | reuse Tailwind scale unless a token helps |

---

## 2. Mantine → RAC component map

Derived from the 17 files importing `@mantine/*`. "Plain HTML" = no RAC
component exists; use a semantic element + Tailwind (as BookForm already
does).

### Interactive (→ RAC components, classless)

| Mantine | Seen in | RAC replacement |
|---|---|---|
| `Button` | page, books/[id], people edit, MainNav, login, account, contact | `Button` (`onPress`) |
| `TextInput` | login, people edit | `TextField` → `Label` + `Input` |
| `Textarea` | people edit | `TextField` → `Label` + `TextArea` |
| `Select` | AuthorFilter | **`ComboBoxField`** (our wrapper) |
| `Menu` | MainNav | `MenuTrigger` + `Menu` + `MenuItem` + `Popover` |
| `Anchor` / `NavLink` | MainNav, TopicsNav | `Link` (active via `aria-current` + `current:`) |
| `Table` | ConditionalTableFields | `Table` / `TableHeader` / `Column` / `TableBody` / `Row` / `Cell` |
| `useDisclosure` (hook) | AppShell, books/[topic] | `useState` boolean (or `Disclosure` if collapsible) |

### Layout / text (→ plain HTML + Tailwind)

| Mantine | RAC | Element |
|---|---|---|
| `Card` | — | `<section>` / `<div>` |
| `Stack` / `Group` / `Box` | — | `<div>` + flex/grid |
| `Title` | — | `<h1>`…`<h3>` |
| `Text` | — | `<p>` / `<span>` |
| `List` | — | `<ul>` / `<li>` |
| `Divider` | `Separator` (or `<hr>`) | `<hr>` |
| `Avatar` | — | `<img>` / `<span>` |
| `Kbd` | — | `<kbd>` |
| `AppShell` + `Burger` | — | layout `<div>` grid + `Button` toggle |

### Infrastructure

| Item | Seen in | Action |
|---|---|---|
| `MantineProvider` / `createTheme` / `@mantine/core/styles.css` | providers.tsx | Remove. RAC needs no provider; delete the Mantine theme + CSS import. |
| `ComboboxItem` / `OptionsFilter` types + `startsWithFilter` | selectFilters.ts | Drop once AuthorFilter moves to `ComboBoxField`; keep `startsWithFilterRA`. |
<!-- | `BookFormOld.tsx` | — | Delete (Mantine backup of the already-migrated form). | NO - I might do that later but you don't delete files -->

---

## 3. State styling checklist (per RAC class)

What each component needs styled beyond its base look. **Focus and selected
are the accessibility-critical ones.**

| RAC element (class) | States to style |
|---|---|
| `react-aria-Input` / `react-aria-TextArea` | `focused`, `hovered`, `disabled`, `invalid`, placeholder |
| `react-aria-Button` | `hovered`, `pressed`, `focus-visible`, `disabled` |
| `react-aria-Checkbox` | `selected`, `indeterminate`, `focus-visible`, `hovered`, `disabled`, `invalid` |
| `react-aria-ToggleButton` (chips) | `selected`, `hovered`, `pressed`, `focus-visible`, `disabled` |
| `react-aria-ListBoxItem` | **`focused` (keyboard highlight — the gap we found)**, `selected`, `hovered`, `disabled` |
| `react-aria-MenuItem` | `focused`, `selected`, `hovered`, `disabled` |
| `react-aria-Popover` | base surface; optional enter/exit |
| `react-aria-Link` | `hovered`, `focus-visible`, `current` |
| `react-aria-Row` / `react-aria-Column` | `hovered`, `selected`, `focus-visible` |
| `react-aria-Switch` | `selected`, `focus-visible`, `hovered`, `disabled` |

---

## 4. Decisions baked in

- **Classless components.** No utility strings in component files; RAC
  defaults + central CSS only. This is what lets a restyle skip the
  components entirely.
- **Multi-select = `ToggleButtonGroup`, not `CheckboxGroup`** — larger,
  tremor-friendly targets (see `BookForm` `formatExtras`).
- **Never colour-only** for state — focus/selected/invalid each need a
  shape, weight, or icon cue too, not just a hue.
- **`menuTrigger`** stays per-field (`ComboBoxField` prop): `focus` for
  short fixed lists, `input` for long/fetched ones.


## Thoughts / upcoming needs

- I don't like the current font and also the colour scheme isn't actually set yet - I'll need to ask you some specifics about that before we go ahead, but I might need other answers first.
- I don't quite understand what RAC system means by "build your own components" - is this basically what we just did with the dropdown/select/combobox? And could this be applied to "missing" components like the "Card" that is the central part of the bibliography page, and really is just a type of styled div that will then loop over a Collection of data? 
- a "show prices" toggle in the avatar popover that makes the page behave as if the user wasn't logged in (without actually changing the role or login status), only available for "family" and "admin" -> using "Switch" component
- if not super complicated: a way to easily make the UI have larger text (Slider or Switch?)
- I'll need a way to show/download a pdf version of a filtered list (but I'm not sure that this is the right place to put this thought)
- is there a way to do something like an A/B test for different styles/versions (as in really big differences) where I can let him choose? That worked really well for the "add person" section. Not everywhere but in some instances this might be important.
- current books page uses the Cards component from mantine, but that isn't that great either, because it doesn't allow for links to be opened in a separate tab, for instance, and also the two buttons to add a price and remove a book don't look great. But this list is absolutely central and the display needs to be as close to a "library catalogue" list as possible. The redesign of that page/components needs to be handled very carefully. I've just created a copy of the book list and single book page to make sure we have a working copy available. The current features that need to remain: displaying information from various sources vertically, not horizontally in cells. I don't want you to create complicated html styles for that just yet because it is really complicated, so let's see what the options are. The thing that also mustn't get lost is that the "return" link on the detail page gets you back to the exact entry you just came from.
- For the detail page, my grandpa was wishing for something that looks more like one of the old library catalogue cards, not stacked in a table, but I'm personally not really a fan of that - but if possible that might be a case for A/B testing.
- I'm not sure how to best do the navigation - the current solution is clunky and doesn't work properly on mobile (a bit on purpose because of the mantine's nav constraints). I feel like NOW is the only time where I can still make big changes because he hasn't really used the new system yet. Maybe having a kind drawer/popover menu he can open and close to make more space for the information on the page might be better, but have it a bit more prominent/accessible on the landing page (which is also still basically empty)
