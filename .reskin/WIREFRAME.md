# Wireframe — Ticker Stage (as built)

Selected direction: **Spectrum Terminal** (`solana-spectrum`) / **Ticker Stage**
(`.reskin/style.json`). Original: `sidebar-workspace` — a fixed 88 px icon rail,
a floating command bar and a two-column split stage on a light canvas.

## Shell

`src/App.vue` renders one linear frame:

```
div.sp-shell
├─ a.sp-skip                        (skip link → #main)
├─ header.sp-masthead               (banner landmark)
│  ├─ RailNav.vue   → div.sp-brand   (mark, Act+oria wordmark, tagline)
│  └─ CommandBar.vue → div.sp-utility (cluster chip, re-read, wallet, menu)
├─ TickerNav.vue    → nav.sp-ticker  (aria-label="Primary", numbered items)
├─ main#main.sp-main
│  ├─ div.sp-notices                (all conditional banners, unchanged)
│  └─ Transition > section.sp-route
│     ├─ header.sp-statement        (eyebrow, h1, deck, actions, proof)
│     └─ section.sp-bands
│        ├─ section.sp-dials        (four beats of huge figures + foot)
│        ├─ div.sp-flow             (article.sp-band ledger bands)
│        └─ section.sp-tail         (wallet / token slabs, notes)
├─ StatusStrip.vue → footer.sp-status (network + session facts, outlined wordmark)
├─ template v-if="menuOpen"         (veil + drawer, id stays `ax-drawer`)
└─ WalletSheet.vue                  (dialog, class-only rewrite)
```

## Composition per route

| Route | Statement band | Bands (in order) |
|---|---|---|
| `/` (home) | eyebrow, "Time on the record.", deck, two actions, three proof items | readout beats, quests ledger, votes ledger with tally, two doors, wallet + token tail, notes |
| `#quests` | running head + deck | filter strip, quest ledger rows, steward publish form |
| `#governance` | running head + deck | filter strip, ballot ledger with split tallies, compose form |
| `#treasury` | running head + deck | meter beats, receipt statement, activity ledger, address tail |
| `#stake` | running head + deck | status definitions, numbered dependency steps, warning note |
| `#learn` | running head + deck | numbered route, checklist, question list |

Every band is full width with a hairline rule and a ghost section index; nothing
keeps the old card surface or the old two-column stage.

## Navigation

A sticky horizontal ticker under the masthead. Each item carries a CSS-counter
index (no new text node), a glyph and the existing route label; the active route
gets a mint underline and `aria-current="page"`. On mobile the ticker scrolls
horizontally and remains keyboard reachable; the drawer keeps the full list.

## CSS

- `src/styles/spectrum.css` — the only imported stylesheet (tokens, base,
  component grammar, responsive rules). `src/styles/bubblegum.css` is retired to
  `.reskin/retired/bubblegum.css` and is no longer in `src/` or imported.
- Namespace `sp-` everywhere; zero shared class tokens with the old `bg-` skin.
- Tokens: black ground `#000`, ink `#fff`, muted `#a6a6aa`, violet `#9945ff`,
  mint `#14f195`, hairline `#29292d`; display "Arial Narrow" stack at 800 with
  -0.055em tracking; mono labels at 0.2em tracking; radii 0–4px.
- Breakpoints: 1080px (beats 2-up), 820px (single column doors/forms, ticker
  scroll), 560px (one beat per row, stacked notice action).

## Kept / removed

- Removed from the render path: the aside narrative column, the icon rail
  (RailNav tab list), the floating command bar, the two-column split stage, the
  light bubblegum token skin and every `bg-` class.
- Kept as content-only children: every route block, conditional branch, drawer,
  wallet sheet, toast, alerts and every binding/handler.
- New: `TickerNav.vue`; `RailNav.vue`, `CommandBar.vue`, `StatusStrip.vue` and
  `WalletSheet.vue` rewritten as presentational pieces with the same props and
  emitted events.
