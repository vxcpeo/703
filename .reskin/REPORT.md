# Reskin report — Rationum

## Direction

- **Style:** Bubblegum Exchange (`uniswap-bubblegum`, clean-fintech) — live-sampled
  from [uniswap.org](https://uniswap.org) (13 349 ms; white ground, no accent
  sampled). 9/10 references sampled OK; Arbitrum returned HTTP 403 and was skipped.
  No reference logo, imagery, copy or code was downloaded or reused.
- **Skeleton:** Split Stage (`split-stage`, spatial).
- **Original:** `terminal-console` (linear) — masthead, sticky numbered ticker strip,
  full-width ruled bands and a status footer on a black canvas with a violet signal.
- **Seed:** `7d3b934c479c6b692ceb89fbb9ca0e8ea17d922269db65906637d0f24a462288`
- **Selection:** the deterministic selector ranked ten directions against the
  original accent `#9945ff`; Bubblegum Exchange scored 0.8973 with an 85 ΔE accent
  shift and paired with Split Stage, a spatial skeleton. Full ranking in
  `.reskin/STYLE.md`.

### What changed structurally

The old shell was a one-dimensional broadcast: masthead with utility bar, a
horizontal numbered ticker, then stacked full-width statement and ledger bands, and
a status footer with an outlined wordmark. The new shell is a split stage: a sticky
42% narrative column carries the brand plate, a vertical numbered index, the route
thesis (kicker, headline, deck, stats, primary actions), the wallet dock and the
colophon, while a 58% scrolling stage carries the route body as floating white panels
(readout figures, ledgers, ballots, meters, receipts, steps, checklist, FAQ). There is
no masthead, no ticker strip, no full-width ruled band, no status footer in the flow,
and no black canvas. The palette moved from black + violet + mint to white + magenta
+ bubble pink.

## Evidence

| Gate | Result |
|---|---|
| Source content contract | **intact** (0 removed, 0 added; 1 binding warning) |
| Contract hash | `053703ed…` (baseline `99fe0a9b…` / frozen `12761c50…`) |
| Rendered content parity (`/`) | **PASS** — 213 stable words, same multiset |
| DOM fingerprint similarity | **0.229** (limit 0.50) |
| Landmark similarity | **0.600** (limit 0.68) |
| CSS class overlap | **0** (limit 0.10) |
| Accent distance | **85.01 ΔE** (`#9945ff` → `#e6006f`; min 30) |
| Contrast failures | **0 / 114** |
| Axe serious/critical | **0** (0 moderate too) |
| Console/page errors | **0** |
| Route status | `/` → 200 |
| Build | `vite build` passed (`.reskin/logs/build.log`) |
| Verdict | **PASS** (`.reskin/verification.json`) |

Screenshots:

- Baseline (before): `.reskin/baseline/home-desktop.png`, `.reskin/baseline/home-mobile.png`
- Current (after): `.reskin/current/home-desktop.png`, `.reskin/current/home-mobile.png`

## Changes

- **New shell:** `src/App.vue` template rebuilt by
  `.reskin/tools/build-split-stage.py`. The `<script setup>` block is byte-for-byte
  unchanged. Every route's statement header was moved into the narrative column
  (content moved, never retyped) and its data body re-wrapped as `div.bz-sheet` inside
  `main.bz-stage`; all presentation class names were remapped through
  `.reskin/tools/class_map.py`.
- **New component roles:** `RailNav.vue` → brand plate, `TickerNav.vue` → vertical
  numbered index, `CommandBar.vue` → wallet dock, `StatusStrip.vue` → colophon,
  `WalletSheet.vue` → wallet picker. Props, emits, handlers, labels and copy are
  unchanged.
- **New token layer:** `src/styles/split-stage.css` (imported from `src/main.js`).
  `src/styles/spectrum.css` retired to `.reskin/retired/spectrum.css`; it is no longer
  imported or present in `src/`.
- **Document chrome:** `website/index.html` theme-color/color-scheme switched to the
  light skin; `og:image:alt` now describes the new card. Meta title/description and
  `lang` are untouched.
- **Social kit:** rebuilt in the same direction by `.rebrand/make_kit.py`
  (`twitter/banner.png`, `twitter/logo.png`, five 1200×630 post cards,
  `twitter/launch-clip.mp4` 1500×500 / 8 s / 15 fps, and the site OG cards). The
  renderer records every string it draws and refuses domains, URLs and handles; no
  social image carries one.

## Accessibility and responsive

- One `h1` per route (in the narrative column), logical `h2`/`h3` order in the stage,
  `aside` (thesis/index), `nav` (index) and `main` landmarks, skip link retained and
  moved first in the DOM.
- Visible focus rings (2 px `--bz-signal-safe`, 2 px offset) on every control; the
  index exposes `aria-current="page"`; the drawer keeps `aria-expanded` /
  `aria-controls`; the wallet picker keeps `role="dialog"` + `aria-modal`.
- Body contrast 0 failures at 4.5:1 / 3:1; axe 0 serious, 0 moderate.
- 390 px: single column, the rail becomes a static header block, the index becomes a
  horizontally scrollable strip that keeps every section reachable, figures stack, no
  horizontal overflow.
- `prefers-reduced-motion` disables the spinner, sheen and page transition.

## Limitations

- Single static route (`/`) with six hash views; `verify.mjs` captures only `/`, while
  the rebrand browser pass captured all six views (`.rebrand/screenshots/`).
- The numbered index adds a presentation-only binding
  (`String(position + 1).padStart(2, "0")`), reported as an additive warning.
- The rendered count gains numeric tokens (index numbers 01–06); numeric drift is a
  warning by design and no stable word changed.
- No git repository exists, so the pre-reskin baseline was captured from a
  reconstructed worktree (`.rebrand/reskin-baseline/website`) built from the rebrand
  apply backup plus the two manual wordmark fixes, because editing had already started
  when the baseline capture was attempted. The baseline contract hash equals the
  frozen pre-reskin hash (`12761c50…`), so the reconstruction is exact.
- The app performs a live Solana Testnet read on mount; the recorded PASS captured
  baseline and current in the same preview state.

The UI was rebuilt around **Bubblegum Exchange** / **Split Stage**; the original
**terminal-console** shell and palette were removed while the content contract stayed
byte-for-byte intact.
