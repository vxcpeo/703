# Split Stage wireframe — Rationum

Selected direction: **Bubblegum Exchange** (`uniswap-bubblegum`) / **Split Stage**
(`split-stage`). Original shell: `terminal-console` (linear broadcast with masthead,
sticky ticker strip and full-width bands).

## Shell

`src/App.vue` renders one shell for all six hash routes:

```
div.bz-app
├── a.bz-skip                      (skip link → #main)
├── div.bz-frame                   (grid: minmax(330px,42fr) / minmax(0,58fr))
│   ├── aside.bz-rail              (sticky, 100vh, own scroll)
│   │   ├── RailNav                brand mark + Ratio/num + tagline
│   │   ├── TickerNav              vertical numbered index (01–06)
│   │   ├── div.bz-rail-thesis     per-route kicker, h1, lede, stats, actions, proof
│   │   ├── CommandBar             cluster chip, re-read, menu, wallet
│   │   └── StatusStrip            colophon: brand, note, explore, network, session, wordmark, fine print
│   └── main#main.bz-stage         (scrolling 58% stage)
│       ├── div.bz-alerts          preview / paused / error / reading notices
│       └── Transition(page)
│           └── section.bz-view
│               └── div.bz-sheet   (per-route body)
├── drawer (menuOpen)
├── toast (txState)
└── WalletSheet (walletPickerOpen)
```

## Route mapping

| Route | Narrative column (sticky) | Scrolling stage |
| --- | --- | --- |
| `#home` | Kicker `SOLANA_NETWORK_NAME · open record`, h1 *Time on the record.*, deck, two primary buttons, three proof facts | Four-figure readout, newest-quest ledger, votes-on-the-floor ledger with leading-proposal tally, two doors, wallet + token note cards |
| `#quests` | Kicker *Participation*, h1 *Find your part in it.*, deck, row/preview stats | Search + filter toolbar, quest entry panels, steward publish form, wallet hint |
| `#governance` | Kicker *Advisory votes*, h1 *Put it to the room.*, deck, proposal stats | Ballot panels with split tallies, compose form, wallet hint |
| `#treasury` | Kicker *Public reads*, h1 *Nothing hidden in the books.*, deck, network stat | Four meter tiles, receipt rows, activity ledger, address note card |
| `#stake` | Kicker *Token details*, h1 *No token is wired up.*, deck, "not configured" stat | Token status facts, dependency steps, wallet hint |
| `#learn` | Kicker *The field guide*, h1 *A way in. A way to check.*, deck, network stat | Numbered steps, FAQ accordion (+/− markers), checklist, connect CTA |

## Components

| Old | New | Notes |
| --- | --- | --- |
| `RailNav.vue` (masthead brand) | brand plate (`bz-mast`) | mark + split wordmark + tagline |
| `TickerNav.vue` (horizontal ticker) | vertical index (`bz-index`, `bz-index-link`) | numbered 01–06, `aria-current="page"` |
| `CommandBar.vue` (floating command bar) | wallet dock (`bz-dock`) | same props/emits, cluster chip + icon buttons + wallet |
| `StatusStrip.vue` (status footer) | colophon (`bz-colophon`) | same content moved into the narrative column |
| `WalletSheet.vue` (modal sheet) | wallet picker (`bz-picker`) | same dialog semantics and handlers |

## Tokens and breakpoints

- New global stylesheet: `src/styles/split-stage.css`, imported from `src/main.js`.
- Token namespace `--bz-*` (bg, surface, ink, muted, signal, signal-safe, bubble, line,
  radii, shadow, motion, spacing). Old `spectrum.css` removed from `src/` to
  `.reskin/retired/spectrum.css` and no longer imported.
- Breakpoints: `1180px` (figures 2-up, notes 1-up), `900px` (single column; rail becomes a
  static header block, index becomes a horizontal scroll strip), `520px` (single-column
  figures, compact ledger rows, stacked alert action, full-width wallet dock).
