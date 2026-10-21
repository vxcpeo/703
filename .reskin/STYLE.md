# Reskin art direction — Bubblegum Exchange

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `uniswap-bubblegum` (clean-fintech)
- **Skeleton:** `split-stage` (spatial)
- **Seed:** `bb33d9a2a378694d6d0e596cbd6731a090117474a060bde73b8c8ffe1052cf3b`
- **Source DNA:** [https://uniswap.org](https://uniswap.org)
- **Live sampled:** yes — https://uniswap.org (6701 ms)
- **Original:** terminal-console / light / accent #ff0000

## Why this direction

The selector sampled 9/10 blockchain references, scored every direction for perceptual distance from the original accent (#ff0000) and background (#000000), added a deterministic seed jitter, and chose Bubblegum Exchange because it is 64 ΔE away from the original accent and pairs with Split Stage, a spatial skeleton rather than the original terminal-console.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| polygon-agora | https://polygon.technology | ok (2996 ms) | #670de5 | #000000 |
| base-cobalt | https://www.base.org | ok (4322 ms) | #0000ff | #dde3e9 |
| ethereum-paper | https://ethereum.org | ok (4571 ms) | #0c5681 | #ffffff |
| solana-spectrum | https://solana.com | ok (7231 ms) | #9945ff | #000000 |
| aave-abyss | https://aave.com | ok (3008 ms) | #ff0000 | #000000 |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| optimism-poster | https://www.optimism.io | ok (7426 ms) | #ff0421 | #fafaf9 |
| uniswap-bubblegum | https://uniswap.org | ok (6701 ms) | — | #ffffff |
| cosmos-orbit | https://cosmos.network | ok (3829 ms) | #40b3ff | #000000 |
| sui-tidal | https://sui.io | ok (4602 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Bubblegum Exchange | 0.9908 | 64.4 | split-stage | yes |
| Cobalt Blueprint | 0.9445 | 176.3 | bento-canvas | yes |
| Tidal Sui | 0.9362 | 146.2 | gallery-scroll | yes |
| Paper Protocol | 0.9201 | 130.1 | split-stage | yes |
| Agora Violet | 0.8921 | 145 | documentary | yes |
| Cosmos Orbit | 0.87 | 144.6 | gallery-scroll | yes |
| Spectrum Terminal | 0.8449 | 146.3 | gallery-scroll | yes |
| Signal Navy | 0.82 | 136.8 | bento-canvas | no |
| Poster Optimism | 0.6583 | 11.4 | gallery-scroll | yes |
| Abyss Liquidity | 0.3029 | 0 | orbital | yes |

## Skeleton brief

**Split Stage** — asymmetric 5/7 or 4/8 split with a sticky narrative column; one side scrolls independently; no top navigation bar; a vertical index sits in the sticky column; headline and primary action share the left stage; data is presented as an annotated ledger, not a card grid.

Navigation: Vertical index in the sticky column; on mobile it becomes a horizontally scrollable index strip above the content.

Structure:
1. sticky 42% narrative column with brand, route index and page thesis
1. scrolling 58% data stage
1. full-width proof band below the split
1. footer set inside the narrative column

Content mapping: The sticky column carries brand, route index, page title and the primary action. The scrolling stage carries the table/list/form. Secondary metrics become annotated rows rather than cards.

Recipe: `.split{display:grid;grid-template-columns:minmax(300px,42fr) minmax(0,58fr);min-height:100vh}.narrative{position:sticky;top:0;height:100vh;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(24px,4vw,64px)}.stage{min-height:100vh;padding:clamp(24px,5vw,80px) clamp(20px,5vw,90px)}`

Risks: sticky column must not hide content on short screens; mobile must not preserve the split

## Design tokens

```css
:root {
  --bg: #ffffff;
  --surface: #F9F8FA;
  --surface-alt: #F2EEF3;
  --ink: #0D0D0D;
  --muted: #6D6A70;
  --accent: #E6006F;
  --accent-safe: #C2005D;
  --accent-2: #FF4DA6;
  --line: #E9E4EB;
  --success: #0F7B4D;
  --danger: #C42B2B;
  --warning: #8A5A00;

  --font-display: "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-body: "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-mono: "SFMono-Regular", "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 600;
  --display-tracking: -0.03em;
  --label-tracking: 0.04em;

  --radius-sm: 12px;
  --radius-md: 22px;
  --radius-lg: 32px;
  --border: 1px solid var(--line);
  --shadow: 0 18px 40px rgba(20, 10, 25, 0.06);

  --motion-duration: 200ms;
  --motion-ease: cubic-bezier(.2,.7,.2,1);
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

- Surface: 1px solid var(--line); radius 22px; shadow 0 18px 40px rgba(20, 10, 25, 0.06).
- Type: display **"Avenir Next", "Segoe UI", system-ui, sans-serif** at weight 600, tracking -0.03em; body **"Avenir Next", "Segoe UI", system-ui, sans-serif**; numerals and micro-labels **"SFMono-Regular", "Cascadia Mono", ui-monospace, monospace**.
- Texture: soft bubbles, gradient orbs, fine dividers, compact trade widgets.
- Motion: smooth, 200ms, cubic-bezier(.2,.7,.2,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: comfortable. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `terminal-console`; the new skeleton is `split-stage`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Bubblegum Exchange / Split Stage; the original terminal-console shell and palette were removed while the content contract stayed byte-for-byte intact."
