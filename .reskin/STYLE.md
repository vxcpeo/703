# Reskin art direction — Spectrum Terminal

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `solana-spectrum` (performance-brutalist)
- **Skeleton:** `ticker-stage` (linear)
- **Seed:** `4ae7e645db31797674a7c2230a0e549bbd6ae910388f61c25de4216d31013567`
- **Source DNA:** [https://solana.com](https://solana.com)
- **Live sampled:** yes — https://solana.com (3145 ms)
- **Original:** sidebar-workspace / light / accent #e6006f

## Why this direction

The selector sampled 9/10 blockchain references, scored every direction for perceptual distance from the original accent (#e6006f) and background (#ffffff), added a deterministic seed jitter, and chose Spectrum Terminal because it is 85 ΔE away from the original accent and pairs with Ticker Stage, a linear skeleton rather than the original sidebar-workspace.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| base-cobalt | https://www.base.org | ok (2353 ms) | #0000ff | #dde3e9 |
| polygon-agora | https://polygon.technology | ok (2691 ms) | #670de5 | #000000 |
| solana-spectrum | https://solana.com | ok (3145 ms) | #9945ff | #000000 |
| ethereum-paper | https://ethereum.org | ok (3930 ms) | #0c5681 | #ffffff |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| uniswap-bubblegum | https://uniswap.org | ok (5031 ms) | — | #ffffff |
| aave-abyss | https://aave.com | ok (4874 ms) | #ff0000 | #000000 |
| optimism-poster | https://www.optimism.io | ok (8080 ms) | #ff0421 | #fafaf9 |
| cosmos-orbit | https://cosmos.network | ok (5959 ms) | #40b3ff | #000000 |
| sui-tidal | https://sui.io | ok (5666 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Spectrum Terminal | 0.9477 | 85 | ticker-stage | yes |
| Agora Violet | 0.9268 | 83.7 | orbital | yes |
| Cosmos Orbit | 0.9198 | 102.3 | documentary | yes |
| Paper Protocol | 0.8404 | 91 | split-stage | yes |
| Signal Navy | 0.8247 | 98.2 | terminal-console | no |
| Cobalt Blueprint | 0.8043 | 115.1 | split-stage | yes |
| Abyss Liquidity | 0.7789 | 61.4 | orbital | yes |
| Tidal Sui | 0.7713 | 93 | bento-canvas | yes |
| Poster Optimism | 0.7234 | 54.4 | documentary | yes |
| Bubblegum Exchange | 0.4988 | 12.2 | bento-canvas | yes |

## Skeleton brief

**Ticker Stage** — horizontal ticker band as primary navigation and status; full-width horizontal sections stacked like a broadcast; oversized figures with hard rules; no sidebar and no conventional top app bar; content reveals in horizontal beats.

Navigation: A ticker strip under the wordmark; route names repeat as short labels; active route is marked by a moving underline. Keyboard arrows move the ticker.

Structure:
1. wordmark + ticker strip
1. full-bleed statement band
1. three horizontal data beats
1. ledger band
1. status footer

Content mapping: Each metric becomes a horizontal beat with a huge figure and a small caption. Tables become full-width ledger bands. Forms become a single horizontal strip with inline labels.

Recipe: `.ticker{display:flex;gap:0;overflow:auto;border-block:1px solid var(--line);white-space:nowrap}.ticker a{padding:14px 22px;border-right:1px solid var(--line)}.beat{display:grid;grid-template-columns:minmax(140px,.6fr) minmax(0,2fr);gap:24px;padding:clamp(24px,4vw,56px) 0;border-bottom:1px solid var(--line)}.figure{font-size:clamp(2.4rem,6vw,6rem);line-height:.9}`

Risks: horizontal overflow must be intentional and keyboard reachable; ticker must not trap focus

## Design tokens

```css
:root {
  --bg: #000000;
  --surface: #0B0B0C;
  --surface-alt: #161618;
  --ink: #FFFFFF;
  --muted: #9B9B9F;
  --accent: #9945ff;
  --accent-safe: #9945ff;
  --accent-2: #14F195;
  --line: #29292D;
  --success: #14F195;
  --danger: #FF5C7A;
  --warning: #FFD166;

  --font-display: "Arial Narrow", "Helvetica Neue", "Segoe UI", sans-serif;
  --font-body: "Helvetica Neue", "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 800;
  --display-tracking: -0.055em;
  --label-tracking: 0.2em;

  --radius-sm: 0px;
  --radius-md: 2px;
  --radius-lg: 4px;
  --border: 1px solid var(--line);
  --shadow: 0 0 40px rgba(153, 69, 255, 0.24);

  --motion-duration: 120ms;
  --motion-ease: cubic-bezier(.2,.9,.1,1);
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

- Surface: 1px solid var(--line); radius 2px; shadow 0 0 40px rgba(153, 69, 255, 0.24).
- Type: display **"Arial Narrow", "Helvetica Neue", "Segoe UI", sans-serif** at weight 800, tracking -0.055em; body **"Helvetica Neue", "Segoe UI", sans-serif**; numerals and micro-labels **"IBM Plex Mono", "Cascadia Mono", ui-monospace, monospace**.
- Texture: spectrum gradient shards, scanline grain, status LEDs, ticker strips.
- Motion: fast, 120ms, cubic-bezier(.2,.9,.1,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: dense. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `sidebar-workspace`; the new skeleton is `ticker-stage`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Spectrum Terminal / Ticker Stage; the original sidebar-workspace shell and palette were removed while the content contract stayed byte-for-byte intact."
