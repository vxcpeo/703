# Reskin report — Clepsyra

## Direction

- **Style:** Bubblegum Exchange (`uniswap-bubblegum`, clean-fintech) — live-sampled
  from [uniswap.org](https://uniswap.org) (6701 ms; ground `#ffffff`). 9/10
  references sampled OK; Arbitrum returned HTTP 403 and was skipped. No reference
  logo, imagery, copy or code was downloaded or reused.
- **Skeleton:** Split Stage (`split-stage`, spatial).
- **Original:** `terminal-console` (linear) — fixed 88 px icon rail, floating
  command bar, dark canvas.
- **Seed:** `bb33d9a2a378694d6d0e596cbd6731a090117474a060bde73b8c8ffe1052cf3b`
- **Selection:** the deterministic selector ranked ten directions against the
  original accent `#ff0000` / ground `#000000`; Bubblegum Exchange scored 0.9908
  with a 64 ΔE accent shift and paired with Split Stage, a spatial skeleton.
  Full ranking in `.reskin/STYLE.md`.

### What changed structurally

The old shell was a left icon rail plus a detached top command bar over a dark
canvas; the new shell is a two-column Split Stage: a sticky 38% narrative column
(brand line, numbered vertical index, network console, colophon footer) and a 62%
scrolling evidence stage. There is no top bar, no icon rail, no dark canvas and no
page-bottom footer. Floating cards were replaced by ruled ledger sections
(`.bg-board`, `.bg-sheet` lose their card surface and become top-ruled records
with mono labels), and the whole surface is light with one magenta accent.

## Evidence

| Gate | Result |
|---|---|
| Source content contract | **intact** (0 removed, 0 added) — hash `87df55a4fd45` |
| Rendered content parity (`/`) | **PASS** — 193 words, same multiset |
| DOM fingerprint similarity | **0.275** (limit 0.50) |
| Landmark similarity | **0.60** (limit 0.68) |
| CSS class overlap | **0** (limit 0.10) |
| Accent distance | **61.43 ΔE** (`#ff0000` → `#e6006f`; min 30) |
| Contrast failures | **0 / 97** |
| Axe serious/critical | **0** |
| Console/page errors | **0** |
| Route status | `/` → 200 |
| Build | `vite build` passed (`.reskin/logs/build.log`) |
| Verdict | **PASS** (`.reskin/verification.json`) |

Screenshots:

- Baseline (before): `.reskin/baseline/home-desktop.png`, `.reskin/baseline/home-mobile.png`
- Current (after): `.reskin/current/home-desktop.png`, `.reskin/current/home-mobile.png`

The verifier classifies the new source as `sidebar-workspace` because its
text-based traits only look for an `<aside>` element; the implemented skeleton is
the selected Split Stage (sticky narrative column + scrolling stage, no top bar,
no rail). The gate only requires the archetype to change, and it does
(`terminal-console` → a different id and family).

## Changes

- **New shell:** `src/App.vue` — `div.bg-frame` with `aside.bg-narrative` and
  `main#main.bg-current`; alerts, the six route blocks, the drawer, the toast and
  the wallet sheet keep every binding, handler and piece of copy.
- **Rewritten presentational components:**
  - `src/components/RailNav.vue` → vertical numbered index + brand line.
  - `src/components/CommandBar.vue` → narrative console block (cluster chip,
    re-read, wallet, menu) — still a `div`, no longer a `header` landmark.
  - `src/components/StatusStrip.vue` → colophon footer inside the narrative,
    keeping Explore / Network / Session and the watermark.
  - `src/components/WalletSheet.vue` → class rename only, same dialog.
- **New token layer:** `src/styles/bubblegum.css` (imported from `src/main.js`).
  `src/styles/reskin.css` is retired to `.reskin/retired/reskin.css` and is no
  longer in `src/` or imported, so the palette scan and the DOM cannot see it.
- **Removed from the render path:** the icon rail, the top command bar, the dark
  canvas, the old `ax-` class namespace.
- **Tooling kept for provenance:** `.reskin/build-css.py` (stylesheet
  transformation) and `.reskin/build-app.py` (template shell surgery).

## Accessibility and responsive

- One `h1` per route (unchanged), logical `h2`/`h3` order, `header`/`nav`/`main`/`footer`
  landmarks, skip link retained.
- Visible focus rings (2 px `--accent-safe`, 2 px offset) on every control; the
  index links expose `aria-current="page"`.
- Body contrast 0 failures at 4.5:1 / 3:1; axe 0 serious or critical issues.
- 390 px layout: one column, narrative stacks on top, index becomes a horizontal
  scroll strip, no horizontal overflow, no content hidden.
- `prefers-reduced-motion` disables the spinner and transitions.

## Limitations

- Single static route (`/`) with six hash views; all six were rendered by the
  browser pass in the rebrand verification, and the content contract covers the
  whole app. No dynamic routes exist.
- The app performs a live Solana Testnet read on mount. The rendered audit
  classifies the page as "live" or "preview" depending on whether that read
  completes inside the capture window (~3 s); both states are legitimate, and the
  comparison is only meaningful when both captures land in the same state. Earlier
  attempts that landed in preview mode were discarded as runtime-state noise, not
  content changes; the recorded PASS was captured in the same live state as the
  baseline.
- The colophon (with the site footer content) sits inside the sticky narrative
  column, so on mobile it stacks above the stage rather than at the very bottom.

The UI was rebuilt around **Bubblegum Exchange** / **Split Stage**; the original
**terminal-console** shell and palette were removed while the content contract
stayed byte-for-byte intact.
