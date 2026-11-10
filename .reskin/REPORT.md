# Reskin report — Docketa, Orbit Ledger

## Direction

- **Style:** Abyss Liquidity (`aave-abyss`, dark-technical) — live-sampled from
  [aave.com](https://aave.com) (1 119 ms; ground `#000000`, accent `#ff0000`).
  8/10 references sampled OK; solana.com returned HTTP 429 and arbitrum.io HTTP 403.
  No reference logo, imagery, copy or code was downloaded or reused.
- **Skeleton:** Orbital (`orbital`, spatial) — circular stage, route nodes on the
  ring, circular core, focused panel below.
- **Original:** `sidebar-workspace` (shell) detected from the previous **Split Stage**
  build — sticky 42 % narrative rail beside a 58 % scrolling stage, white ground,
  magenta `#e6006f` signal.
- **Seed:** `b8e86a32…` (selector output, `.reskin/STYLE.md`).
- **Selection:** the selector ranked ten directions against the original accent
  `#e6006f` and chose Abyss Liquidity (0.9255, 61.4 ΔE) paired with Orbital, a
  spatial skeleton rather than the previous shell.

### What changed structurally

The previous shell was a two-column split: a sticky rail carrying brand, a vertical
numbered index, the route thesis, the wallet dock and the colophon, beside a stage of
stacked white panels on a pink-white ground. The new shell is a single circular stage:
the brand seal sits at the top, six route nodes are placed on a ring, the route title
lives in a circular core at the centre, the deck (lede, primary actions, stats) hangs in
the ring's lower aperture, and a floating dock is pinned to the viewport corner. The
route body is a focused panel that overlaps the orbit's bottom edge and is split into a
band column plus a marginal column (no notes nested inside the band). The colophon has
left the aside entirely and is now a page footer with a rim arc and an oversized
wordmark. The palette moved from white + magenta + bubble pink to black + signal red +
teal current; the ground is black, the type is Trebuchet/Segoe with mono metadata.

## Evidence

| Gate | Result |
|---|---|
| Source content contract | **intact** (0 removed, 0 added, 0 warnings) |
| Contract hash | `ce9228ec8b28…` (baseline and current agree) |
| Rendered content parity (`/`) | **PASS** — 199 stable words, same multiset |
| DOM fingerprint similarity | **0.455** (limit 0.50) |
| Landmark similarity | **0.333** (limit 0.68) |
| CSS class overlap | **0** (limit 0.10) |
| Accent distance | **61.43 ΔE** (`#e6006f` → `#ff0000`; min 30) |
| Contrast failures | **0 / 95** |
| Axe serious/critical | **0** (0 moderate too) |
| Console/page errors | **0** |
| Route status | `/` → 200 |
| Build | `vite build` passed (`.reskin/logs/build.log`) |
| Behaviour smoke test | **16/16 pass** (`.reskin/tools/behaviour.mjs`) |
| Verdict | **PASS** (`.reskin/verification.json`) |

Screenshots:

- Before: `.reskin/baseline/home-desktop.png`, `.reskin/baseline/home-mobile.png`
- After: `.reskin/current/home-desktop.png`, `.reskin/current/home-mobile.png`
- All six views: `.reskin/views/final-{home,quests,governance,treasury,stake,learn}-{desktop,mobile}.png`
- The social kit built from these surfaces is reported in `703/twitter/REPORT.md`.

## Changes

- **New shell:** `src/App.vue` template rebuilt by
  `.reskin/tools/restructure.py`. `<header class="orb-hero">` carries the ring art
  (`orb-rings`, four strokes + conic sweep), the brand seal, `orb-system` (ring +
  `orb-index` + `orb-core`), the `orb-dispatch` deck and the `StageDock`. `<main>` holds
  the panel; `<footer class="orb-colophon">` follows it. The `<script setup>` block is
  untouched except for the five component imports.
- **New components:** `BrandSeal.vue` (brand plate), `OrbitIndex.vue` (route nodes on
  the ring, `--a` angles in CSS), `StageDock.vue` (cluster chip, refresh, menu, wallet),
  `RingColophon.vue` (outer-ring footer), `WalletPicker.vue` (wallet dialog, same
  `role="dialog"` and id). Props, emits, `aria-label`s and handlers are unchanged.
- **Retired:** `RailNav.vue`, `TickerNav.vue`, `CommandBar.vue`, `StatusStrip.vue`,
  `WalletSheet.vue` and `src/styles/split-stage.css` moved to `.reskin/retired/`; none
  is imported or rendered.
- **New token layer:** `src/styles/orbit.css` (imported from `src/main.js`). No
  `bz-`/`bg-`/`sp-` selector survives in the render path
  (`.reskin/tools/rename-classes.py` maps all 205 old class names onto the orbit
  vocabulary).
- **Route composition:** each `.orb-canvas--<route>` is a focused panel with a band
  column and a marginal column at ≥900 px (7/5, 8/4, 6.5/5.5), single column below.
  Home adds `orb-colonnade` around the two ledgers; the two doors are a wide/narrow pair
  with an offset. Treasury dials keep a 2×2 arc group; the statement keeps its leader
  dots; the FAQ keeps `details`/`summary` with a `+`/`−` marker.
- **Document chrome:** `website/index.html` theme-color `#000000`, `color-scheme`
  `dark`, `og:image:alt` rewritten for the dark card. Title, description, `lang` and
  all social meta strings are untouched. The brand mark SVGs were recoloured from
  `#e6006f` to `#ff0000`; geometry and `aria-label` unchanged.

## Accessibility and responsive

- One `h1` per route (inside the core), logical `h2`/`h3` order in the panel and the
  footer, `header`/`nav`/`main`/`footer` landmarks, skip link retained and first in the
  DOM.
- Visible focus rings (2 px teal `--accent-2`, 3 px offset) on every control; the orbit
  index exposes `aria-current="page"`; the drawer keeps `aria-expanded` /
  `aria-controls`; the wallet picker keeps `role="dialog"` + `aria-modal`.
- Body contrast 0 failures at 4.5:1 / 3:1 on the black ground; axe clean.
- 900 px: the nodes leave the ring and become a staggered two/three-column arc under the
  seal, the core keeps its halo, the panel collapses to one column. 390 px: core 310 px,
  dock spans the viewport width, no horizontal overflow on any of the six views
  (`.reskin/views`), alerts wrap.
- `prefers-reduced-motion: reduce` disables the loading scan, the dock pulse and the page
  transition.

## Limitations

- Single static route (`/`) with six hash views. `verify.mjs` captures `/`, while
  `.reskin/tools/shots.mjs` captures all six views (desktop + mobile, no console errors,
  no overflow).
- The live sample returned `#ff00ff` as the secondary accent for `aave-abyss`; that is
  the same magenta family as the removed brand accent, so it is rejected under
  originality guard 2 and replaced with the catalog's teal `#2EBAC6`. The primary accent
  stays at the sampled `#ff0000` (61.43 ΔE).
- The app performs a live Solana Testnet read on mount, so panel counts switch between
  preview and live values between captures; numeric tokens are compared as a warning
  only and no stable word changes.
- The previous Split Stage evidence was archived to
  `703/.reskin-archive/website-20261022-split-stage/` and is intentionally outside the
  Vue root so it is not scanned as project source.

The UI was rebuilt around **Abyss Liquidity** / **Orbital**; the original
**sidebar-workspace** shell and palette were removed while the content contract stayed
byte-for-byte intact.
