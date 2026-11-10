# Wiring plan — Abyss Liquidity / Orbital

Committed direction from `.reskin/style.json` (selector output, not a suggestion):

- Style: `aave-abyss` **Abyss Liquidity** — dark-technical, nocturnal, liquid glass.
- Skeleton: `orbital` — spatial. The previous shell was a **Split Stage**
  (sticky 42% narrative rail beside a 58% scrolling stage); that shell is deleted.
- Accent: `#ff0000` (61.4 ΔE from the removed `#e6006f`). Secondary `#2EBAC6`
  from the style catalog (the live sample returned `#ff00ff`, which is the same
  magenta family as the removed brand accent, so it is rejected under
  originality guard 2 and replaced by the catalog's teal).

## Shell

One shell for all six hash routes: **Orbit Ledger**.

```
.orb-field  (app root, near-black canvas, radial haze)
├─ a.orb-skip                              (existing "Skip to content")
├─ header.orb-hero                         (banner landmark, no app bar)
│  ├─ .orb-rings  ×4 ring strokes + conic sweep + 24 tick marks  (aria-hidden)
│  ├─ BrandSeal  → .orb-seal                (wordmark + tagline, top centre)
│  ├─ OrbitIndex → nav.orb-index             (6 route nodes on the ring)
│  ├─ .orb-core  (circle)                   (route kicker + h1 + stats/proof)
│  ├─ .orb-dispatch                         (route lede + primary actions)
│  └─ .orb-dock  (fixed corner dock)        (cluster chip, refresh, menu, wallet)
├─ main#main.orb-stage                      (focused content panel)
│  ├─ .orb-alerts
│  └─ section.orb-view > .orb-canvas        (per-route composition)
│     ├─ .orb-band       (primary routed band, full width)
│     ├─ .orb-colonnade  (asymmetric 12-col grid: 7/5, 5/7, 4/8 offsets)
│     └─ .orb-margin     (marginal notes as a ring of cards)
├─ footer.orb-colophon                      (RingColophon, outer-ring footer)
├─ drawer (unchanged behaviour, new markup)
├─ toast
└─ WalletPicker (role=dialog, unchanged behaviour)
```

### Component roles

| Old file | New file | Role now |
|---|---|---|
| `components/RailNav.vue` | `components/BrandSeal.vue` | brand seal at the top of the orbit |
| `components/TickerNav.vue` | `components/OrbitIndex.vue` | route nodes on the ring (circular on desktop, vertical arc on mobile) |
| `components/CommandBar.vue` | `components/StageDock.vue` | floating corner dock |
| `components/StatusStrip.vue` | `components/RingColophon.vue` | outer-ring footer |
| `components/WalletSheet.vue` | `components/WalletPicker.vue` | wallet dialog (same props/emits/ids) |

Props, emits, labels, `id`s and handlers are unchanged. `App.vue`'s
`<script setup>` block is not edited.

## Route compositions

| Route | Composition (all existing copy, moved not retyped) |
|---|---|
| `#home` | Orbit hero → band "On the record today" with four figures on a radial arc + live foot → 7/5 colonnade: quest ledger sheet / ballot sheet with a circular tally → two wide doors, offset → marginal ring: wallet card, token card, "Before you sign" hint |
| `#quests` | Orbit hero → toolbar as a pill dock (search, chips, count) → quest rows as orbit rows with capacity gauges in a 7-col ledger, publish form + hint in the 5-col margin |
| `#governance` | Orbit hero → ballot cards with split tallies in the 7-col ledger; compose editor + "What lands" steps in the 5-col margin; advisory hint spans |
| `#treasury` | Orbit hero → four meter dials on a radial arc, receipt rows as a ruled statement, activity panel; addresses + warning in the margin |
| `#stake` | Orbit hero → token status facts and the ordered "What has to exist first" steps; wiring card + "No mint has been issued" in the margin |
| `#learn` | Orbit hero → three numbered steps as framed scenes, FAQ as a rules accordion; checklist + sample-rows hint in the margin |

## CSS

- New single global stylesheet `src/styles/orbit.css` (imported from `src/main.js`).
- `src/styles/split-stage.css` moves to `.reskin/retired/split-stage.css`; it is
  not imported and no `bz-`/`bg-`/`sp-` rule survives in the render path.
- Tokens (from `STYLE.md`, plus orbital extras):
  `--field #000000`, `--shell #111A24`, `--shell-2 #182533`, `--ink #F4F7FA`,
  `--dim #8FA3B5`, `--signal #ff0000`, `--signal-soft #FF5C5C`,
  `--current #2EBAC6`, `--rule #1E2A36`, `--good`, `--bad`, `--warn`.
- Breakpoints: `1180px` (ring shrinks, nodes move inward), `900px` (nodes leave
  the ring and become a 2-col vertical arc under the core), `560px` (single
  column, dock compresses to icon buttons).
- Motion: 240ms `cubic-bezier(.22,1,.36,1)`; every non-essential animation is
  wrapped in `@media (prefers-reduced-motion: no-preference)`.

## Content lock

Every visible string, placeholder, `alt`, `title`, `aria-label`, binding,
handler, link target, form field and hidden text in
`.reskin/content-contract.json` is preserved with its exact occurrence count.
The only permitted additions are `aria-*` names for new presentation controls,
and they reuse existing labels.
