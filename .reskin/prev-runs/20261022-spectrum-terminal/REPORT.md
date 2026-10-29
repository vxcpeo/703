# Reskin report — Actoria

## Direction

- **Style:** Spectrum Terminal (`solana-spectrum`, performance-brutalist) —
  live-sampled from [solana.com](https://solana.com) (3145 ms; ground `#000000`).
  9/10 references sampled OK; Arbitrum returned HTTP 403 and was skipped. No
  reference logo, imagery, copy or code was downloaded or reused.
- **Skeleton:** Ticker Stage (`ticker-stage`, linear).
- **Original:** `sidebar-workspace` (shell) — fixed 88 px icon rail, floating
  command bar, two-column split stage on a light canvas with a magenta signal.
- **Seed:** `4ae7e645db31797674a7c2230a0e549bbd6ae910388f61c25de4216d31013567`
- **Selection:** the deterministic selector ranked ten directions against the
  original accent `#e6006f`; Spectrum Terminal scored 0.9477 with an 85 ΔE
  accent shift and paired with Ticker Stage, a linear skeleton. Full ranking in
  `.reskin/STYLE.md`.

### What changed structurally

The old shell was a left icon rail plus a floating command bar over a light
two-column split stage; the new shell is a linear broadcast: masthead, sticky
numbered ticker, full-width statement band per route, then ruled bands (four-beat
readout, ledger rows, split tallies, receipt rows, steps, accordion) and a status
footer with a large outlined wordmark. There is no sidebar, no icon rail, no card
surface, no floating command bar and no light canvas. The palette moved from
white + magenta to black + violet with one mint accent.

## Evidence

| Gate | Result |
|---|---|
| Source content contract | **intact** (0 removed, 0 added) — hash `2cd00ec3` |
| Rendered content parity (`/`) | **PASS** — 213 words, same multiset |
| DOM fingerprint similarity | **0.375** (limit 0.50) |
| Landmark similarity | **0.30** (limit 0.68) |
| CSS class overlap | **0** (limit 0.10) |
| Accent distance | **85.01 ΔE** (`#e6006f` → `#9945ff`; min 30) |
| Contrast failures | **0 / 114** (baseline had 4) |
| Axe serious/critical | **0** |
| Console/page errors | **0** |
| Route status | `/` → 200 |
| Build | `vite build` passed (`.reskin/logs/build.log`) |
| Verdict | **PASS** (`.reskin/verification.json`) |

Screenshots:

- Baseline (before): `.reskin/baseline/home-desktop.png`, `.reskin/baseline/home-mobile.png`
- Current (after): `.reskin/current/home-desktop.png`, `.reskin/current/home-mobile.png`

## Changes

- **New shell:** `src/App.vue` template rebuilt by
  `.reskin/tools/build-spectrum.py` (the `<script setup>` block is byte-for-byte
  unchanged). The split-stage aside, wide/margin columns and card wrappers were
  replaced with `header.sp-masthead`, `nav.sp-ticker`, `main.sp-main`,
  `header.sp-statement`, `section.sp-bands`, `section.sp-tail` and
  `footer.sp-status`; every band gained an inner wrapper, board sections became
  `article` elements, ledgers and checklists became ordered lists.
- **New component:** `src/components/TickerNav.vue` (horizontal numbered ticker).
- **Rewritten presentational components:**
  - `RailNav.vue` → brand block (mark, split wordmark, tagline).
  - `CommandBar.vue` → utility strip (cluster chip, re-read, wallet, menu).
  - `StatusStrip.vue` → status footer (Explore / Network / Session, outlined
    wordmark, fine print).
  - `WalletSheet.vue` → new classes, same dialog and handlers.
- **New token layer:** `src/styles/spectrum.css`, imported from `src/main.js`.
  `src/styles/bubblegum.css` is retired to `.reskin/retired/bubblegum.css` and is
  no longer in `src/` or imported.
- **Removed from the render path:** the icon rail, the floating command bar, the
  split-stage narrative column, the light canvas and the whole `bg-` class
  namespace.

## Social kit (same direction)

The Twitter kit was rebuilt in the same Spectrum Terminal direction during this
pass: `twitter/banner.png` (1500×500), `twitter/logo.png` (1024×1024), the five
1200×630 post cards, `twitter/launch-clip.mp4` (1500×500, 8 s, 15 fps, 120
frames) and the four OG/link cards. They use the same black/violet/mint palette,
condensed display type, mono labels and ticker strip. Per `twitter/content.txt`,
no social image carries a domain, URL or handle (the site OG card is the one
exception, as a link card); the renderer in `.rebrand/make_kit.py` records every
string it draws and refuses domains, URLs and handles.

## Accessibility and responsive

- One `h1` per route, logical `h2`/`h3` order, `header`/`nav`/`main`/`footer`
  landmarks, skip link retained.
- Visible focus rings (2 px mint, 2 px offset) on every control; the ticker
  exposes `aria-current="page"`; the drawer keeps `aria-expanded`/`aria-controls`.
- Body contrast 0 failures at 4.5:1 / 3:1 (baseline had 4); axe 0 serious or
  critical issues.
- 390 px layout: single column, ticker scrolls horizontally, beats stack, no
  horizontal overflow, no content hidden.
- `prefers-reduced-motion` disables the spinner and transitions.

## Limitations

- Single static route (`/`) with six hash views; all six render from the same
  markup and were captured in the rebrand browser pass. No dynamic routes exist.
- The app performs a live Solana Testnet read on mount. The footer's "last read"
  value (or "Not yet") and the live/preview banner depend on whether that read
  completes inside the capture window. The recorded PASS captured baseline and
  current in the same preview state; runs that landed in different states were
  discarded as runtime-state noise, not content changes.
- The baseline evidence was recaptured once from a restored copy of the
  pre-reskin source after an editing step double-encoded two footer characters
  (`©`, `·`). The corrected baseline strings are the true pre-reskin characters
  and the reskin report's contract hash covers the corrected snapshot.

The UI was rebuilt around **Spectrum Terminal** / **Ticker Stage**; the original
**sidebar-workspace** shell and palette were removed while the content contract
stayed byte-for-byte intact.
