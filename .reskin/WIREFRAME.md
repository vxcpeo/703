# Wireframe — Split Stage (as built)

Selected direction: **Bubblegum Exchange** / **Split Stage** (`.reskin/style.json`).
Original: **terminal-console** (linear), a fixed 88 px icon rail plus a floating
command bar over a dark canvas.

## Shell

`src/App.vue` renders one frame and two regions:

```
div.bg-frame  (grid: minmax(300px, 38fr) / minmax(0, 62fr))
├─ a.bg-skip                      (skip link → #main)
├─ aside.bg-narrative             (position: sticky; top: 0; height: 100vh)
│  ├─ RailNav  → nav.bg-index     (brand line + numbered vertical index)
│  ├─ CommandBar → div.bg-console (cluster chip, re-read, wallet, menu)
│  └─ StatusStrip → footer.bg-colophon (brand, Explore/Network/Session, watermark, fine print)
├─ template v-if="menuOpen"       (veil + drawer, id stays `ax-drawer` for the ARIA target)
└─ main#main.bg-current           (the scrolling evidence stage)
   ├─ div.bg-alerts               (all conditional banners, unchanged)
   └─ Transition > section.bg-view (the same six route blocks)
      ├─ template v-if="route === 'home'"       …
      ├─ template v-if="route === 'quests'"     …
      ├─ template v-if="route === 'governance'" …
      ├─ template v-if="route === 'treasury'"   …
      ├─ template v-if="route === 'stake'"      …
      └─ template v-if="route === 'learn'"      …
```

## Composition per route

Every route keeps its existing blocks (runhead, readout, boards, sheets, forks,
meters, statements, steps, FAQ, forms) and every binding/handler. The skeleton
change is at the frame level and in the grammar of those blocks:

| Route | Narrative column | Stage composition |
|---|---|---|
| `/` (home) | brand, numbered index, console, colophon | running hero, four-cell readout panel, ruled quest ledger, ballot ledger, two "fork" panels, wallet/token marginalia, ledger footer |
| `#quests` | same | running head + filter strip, quest ledger rows, filters, steward form |
| `#governance` | same | running head, ballot ledger with split tally bars, compose drawer |
| `#treasury` | same | running head, receipt-style statement rows, addresses, activity ledger |
| `#stake` | same | running head, status definitions as ruled steps |
| `#learn` | same | running head, numbered route, checklist, question list |

Cards that used to float are restyled as ruled records (`.bg-board`, `.bg-sheet`
lose their card surface and become top-ruled ledger sections with mono labels).
The one surviving "panel" is the readout anchor, which keeps the accent wash.

## Navigation

Vertical numbered index inside the sticky narrative (CSS counter, so no new text
nodes). On mobile (`max-width: 1023px`) the whole narrative stacks above the
stage and the index becomes a horizontally scrollable strip; the `aria-current`
state and the keyboard order are unchanged.

## CSS

- `src/styles/bubblegum.css` — the only imported stylesheet (token layer + base +
  component grammar + Split Stage shell). `src/styles/reskin.css` is retired to
  `.reskin/retired/reskin.css` (not imported, not in `src/`).
- Namespace `bg-` everywhere; zero shared class tokens with the old `ax-` skin.
- Tokens: white ground, `#0d0d0d` ink, `#6d6a70` muted, one magenta accent
  `#e6006f` (`#c2005d` for text-bearing fills), `#e9e4eb` rules, 12/22/32 px radii.

## Deleted / kept

- Deleted from the render path: the icon rail, the floating command bar, the dark
  canvas, the old `reskin.css` token skin.
- Kept as content-only children: every route block, all conditional branches,
  the drawer, the wallet sheet, the toast.
- `WalletSheet.vue` keeps its dialog structure with renamed classes.
