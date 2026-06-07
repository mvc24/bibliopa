# Brief for claude.ai/design — Bibliopa visual system

Paste into claude.ai/design. **Goal:** decide the visual look (palette, type,
spacing) so we can transcribe the values into CSS tokens. The output we need
is concrete values mapped to the roles listed at the bottom.

## Context
- A German-language web app: a personal book bibliography (~20,000 entries)
  built for the developer's 90-year-old grandfather.
- He is the primary user: **low vision** and a **hand tremor**.
- **Desktop-first** (mobile barely used).
- Feel: calm, legible, like a well-kept library / archive catalogue. Not flashy.

## Hard accessibility requirements (non-negotiable)
- Body text contrast **≥ 7:1** against its background (WCAG AAA); never below 4.5:1.
- Borders, icons, focus rings, UI edges **≥ 3:1** contrast.
- Base font size **≥ 18px**. The design must also hold up at the two larger
  steps below.
- Minimum interactive target **44×44px** (tremor).
- Always-visible, high-contrast **focus indicator** (≥ 2px, with offset).
- State (selected / focus / error) must **never be colour-only** — also use
  weight, underline, border, or an icon.

## Font-size Switch (please design for all three steps)
A control (a Switch, or 3 buttons) scales the whole UI from the root font size:
- **Normal** = 18px (scale 1.0)
- **Large** = 21px (scale ~1.15)
- **Larger** = 24px (scale ~1.3)

Everything is in `rem`, so it all scales together. Please show the busiest
screen (the catalogue list) at **Normal** and at **Larger** so we can check it
still holds together.

## Aesthetic input needed from the design
- **Font:** I want you to use Adobe Jenson Pro, I've added it to a project <link rel="stylesheet" href="https://use.typekit.net/eiy0qlm.css">
- **Palette:** here are some suggestions: #0c2029, #8a6c49, #4c615a, #493d2d

## Screens to mock (so the system is tested against real layouts)
1. Top bar + a collapsible left sidebar listing ~50 topics (his data index).
2. Catalogue list — rows of book entries, info stacked **vertically** (like a
   library catalogue card), each row with a link + small action buttons.
3. Book detail page.
4. A form with text fields, comboboxes, toggle-button groups, buttons.
5. The font-size Switch.

## Token roles to fill (give a concrete value for each)
- **Colour:** background, foreground (body text), surface (cards/popovers/menus),
  surface-foreground, border, primary (action) + on-primary, selected +
  on-selected, hover, muted-foreground, focus-ring, invalid.
- **Type:** font family; sizes base / sm / lg / xl / 2xl; weights normal /
  medium / bold; line-heights.
- **Sizing:** target-min (44px), control height, radius, border-width,
  focus-ring width + offset.

## Output format
Concrete values — hex, font names, px/rem — mapped to the roles above, so they
drop straight into our CSS tokens (`globals.css @theme`).
