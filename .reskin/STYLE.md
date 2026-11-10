# Reskin art direction — Abyss Liquidity

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `aave-abyss` (dark-technical)
- **Skeleton:** `orbital` (spatial)
- **Seed:** `b8e86a32974e202e3fde9f5d3566cf2754298e47a5aec047bcabe2394703fa2d`
- **Source DNA:** [https://aave.com](https://aave.com)
- **Live sampled:** yes — https://aave.com (1119 ms)
- **Original:** sidebar-workspace / light / accent #e6006f

## Why this direction

The selector sampled 8/10 blockchain references, scored every direction for perceptual distance from the original accent (#e6006f) and background (#ffffff), added a deterministic seed jitter, and chose Abyss Liquidity because it is 61 ΔE away from the original accent and pairs with Orbital, a spatial skeleton rather than the original sidebar-workspace.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| solana-spectrum | https://solana.com | failed: HTTP 429 | — | — |
| ethereum-paper | https://ethereum.org | ok (909 ms) | #0c5681 | #ffffff |
| base-cobalt | https://www.base.org | ok (1315 ms) | #0000ff | #dde3e9 |
| polygon-agora | https://polygon.technology | ok (1314 ms) | #670de5 | #000000 |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| aave-abyss | https://aave.com | ok (1119 ms) | #ff0000 | #000000 |
| optimism-poster | https://www.optimism.io | ok (2366 ms) | #ff0421 | #fafaf9 |
| uniswap-bubblegum | https://uniswap.org | ok (2304 ms) | — | #ffffff |
| cosmos-orbit | https://cosmos.network | ok (1918 ms) | #40b3ff | #000000 |
| sui-tidal | https://sui.io | ok (2263 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Abyss Liquidity | 0.9255 | 61.4 | orbital | yes |
| Cosmos Orbit | 0.8239 | 102.3 | orbital | yes |
| Spectrum Terminal | 0.8048 | 70.5 | terminal-console | no |
| Agora Violet | 0.7992 | 83.7 | orbital | yes |
| Paper Protocol | 0.7638 | 91 | split-stage | yes |
| Signal Navy | 0.7544 | 98.2 | command-rail | no |
| Cobalt Blueprint | 0.7462 | 115.1 | split-stage | yes |
| Tidal Sui | 0.7257 | 93 | gallery-scroll | yes |
| Poster Optimism | 0.6357 | 54.4 | documentary | yes |
| Bubblegum Exchange | 0.3866 | 12.2 | orbital | yes |

## Skeleton brief

**Orbital** — centered radial composition with concentric rings; route navigation arranged around the primary object; content revealed in a focused panel inside the orbit; very few straight edges; circular masks and arcs; large empty space around the core.

Navigation: Circular route ring around the core with accessible names; keyboard tab order follows the ring; mobile becomes a vertical arc.

Structure:
1. core object with the page's primary figure
1. orbit ring with routes
1. focused content panel
1. secondary arc of metrics
1. footer on the outer ring

Content mapping: The primary metric becomes the core. Secondary metrics sit on the inner ring. Tables become a focused panel with a record switcher. Forms become a side panel that opens from the ring.

Recipe: `.orbit{position:relative;min-height:100svh;display:grid;place-items:center}.ring{position:absolute;inset:8%;border:1px solid var(--line);border-radius:50%}.core{width:min(46vw,520px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,var(--surfaceAlt),var(--surface))}.route{position:absolute;left:50%;top:50%;transform:rotate(var(--a)) translateX(var(--r)) rotate(calc(-1 * var(--a)))}`

Risks: circular layouts can break reading order; DOM order must match visual order; must collapse to a linear layout on mobile

## Design tokens

```css
:root {
  --bg: #000000;
  --surface: #111A24;
  --surface-alt: #182533;
  --ink: #F4F7FA;
  --muted: #8FA3B5;
  --accent: #ff0000;
  --accent-safe: #ff0000;
  --accent-2: #ff00ff;
  --line: #1E2A36;
  --success: #5CE1A0;
  --danger: #FF7A7A;
  --warning: #F2C94C;

  --font-display: "Trebuchet MS", "Segoe UI", sans-serif;
  --font-body: "Segoe UI", "Helvetica Neue", sans-serif;
  --font-mono: "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 650;
  --display-tracking: -0.035em;
  --label-tracking: 0.1em;

  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --border: 1px solid rgba(143, 163, 181, 0.18);
  --shadow: 0 26px 70px rgba(0, 0, 0, 0.5);

  --motion-duration: 240ms;
  --motion-ease: cubic-bezier(.22,1,.36,1);
  --space-1: clamp(4px, .35vw, 6px);
  --space-2: clamp(8px, .7vw, 12px);
  --space-3: clamp(14px, 1.2vw, 20px);
  --space-4: clamp(22px, 2vw, 32px);
  --space-5: clamp(36px, 3.4vw, 56px);
  --space-6: clamp(56px, 5vw, 88px);
  --page-pad: clamp(18px, 4vw, 64px);
  --max-width: 1440px;
}
```

## Component grammar

- Surface: 1px solid rgba(143, 163, 181, 0.18); radius 16px; shadow 0 26px 70px rgba(0, 0, 0, 0.5).
- Type: display **"Trebuchet MS", "Segoe UI", sans-serif** at weight 650, tracking -0.035em; body **"Segoe UI", "Helvetica Neue", sans-serif**; numerals and micro-labels **"Cascadia Mono", ui-monospace, monospace**.
- Texture: liquid glass, teal-magenta glow, fine grid, data sparklines.
- Motion: fluid, 240ms, cubic-bezier(.22,1,.36,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: comfortable. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `sidebar-workspace`; the new skeleton is `orbital`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Abyss Liquidity / Orbital; the original sidebar-workspace shell and palette were removed while the content contract stayed byte-for-byte intact."
