# Reskin wireframe — Attesio

Selected direction: **Abyss Liquidity** (`aave-abyss`) / **Command Rail** (`command-rail`).
Original: `dashboard-shell` (top masthead with six icon pills, centred paper column, card grids).

## New shell

| Piece | File | Role |
|---|---|---|
| `AxDesk` root | `src/App.vue` | page frame, alerts, route stage |
| `RailNav` | `src/components/RailNav.vue` | fixed 88px glyph spine: rotated wordmark block at the head, six route glyphs with vertical micro-labels, badge dots |
| `CommandBar` | `src/components/CommandBar.vue` | floating/sticky command bar 16px off the top: cluster chip, re-read, wallet, sections toggle |
| `StatusStrip` | `src/components/StatusStrip.vue` | bottom status strip: brand, tagline, note, Explore/Network/Session facts, oversized wordmark, fine print |
| `WalletSheet` | `src/components/WalletSheet.vue` | right-hand wallet sheet (`role="dialog"`), new markup and class layer |

Old shell components `SiteHeader.vue`, `SiteFooter.vue` and the global `src/style.css` are deleted.
`main.js` imports `src/styles/reskin.css` only.

## Landmarks

`header.ax-command` → `nav.ax-rail[aria-label=Primary]` → `main#main` (contains the running head and one `aside.ax-margin`) → `footer.ax-status` (contains `nav[aria-label=Footer]`).
No `<header>` inside cards (the old four card headers are gone), so the landmark tree is materially shorter than the original.

## Route compositions

| Route | Running head | Wide column | Marginal column |
|---|---|---|---|
| `#home` | kicker · display h1 · lede · two actions · three facts | live readout strip (4 cells) → quest ledger → vote ledger with tally → two "doors" (Take part / Weigh in) | wallet sheet, token sheet, sign note |
| `#quests` | kicker · h1 · lede · tags | command line (search + filters + count) → quest ledger rows (index, title, detail, gauge, expiry, actions) | steward publish form, wallet note |
| `#governance` | kicker · h1 · lede · tags | ballot rows (id, status, statement, split tally, legend, vote actions) → advisory note | compose sheet (disclosure + editor), "What lands" steps |
| `#treasury` | kicker · h1 · lede · tags | four-meter strip → account statement (receipt rows) → activity | addresses, warning note |
| `#stake` | kicker · h1 · lede · tags | token status fact list → "What has to exist first" steps | wiring, warning note |
| `#learn` | kicker · h1 · lede · tags | three ways through → FAQ disclosure list | checklist, sample-rows note |

Every route opens with the same running head and resolves into the same `wide + marginal` stage, so the skeleton is recognisably one system while each route's interior differs from the original card grid.

## Mobile

- The rail becomes a **top icon strip** (sticky, 64px, horizontally scrollable, labels kept) instead of a 240px drawer.
- The command bar stays sticky below it, full width minus 12px margins.
- The stage collapses to one linear column: wide column first, marginal column after it.
- The sections drawer (existing `menuOpen` state) remains available from the command bar as a secondary index and wallet panel.

## Tokens and breakpoints

- New token layer in `src/styles/reskin.css`: `--bg #000000`, `--surface #111A24`, `--surface-alt #182533`, `--ink #F4F7FA`, `--muted #8FA3B5`, `--accent #ff0000`, `--accent-2 #ff00ff`, `--line #1E2A36`, plus radii, motion and spacing scales.
- Class namespace `ax-`; no original class name is reused except the framework transition name `page` required by the content contract and `visually-hidden` (new name) for the two screen-reader strings.
- Breakpoints: `1100px` (rail narrows, stage gutter shrinks), `900px` (rail → top strip, stage → single column), `600px` (type and spacing compaction).

## Content handling

Every visible string, placeholder, binding, event handler, icon, form field, route label and asset source from `.reskin/baseline/content-contract.json` is moved verbatim into the new markup. No visible copy is added; icon-only controls use existing labels or accessibility-only names.
