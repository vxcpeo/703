# Reskin inventory — clepsyra-web

Generated: 2026-10-20T15:40:00.563Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/703/website` |
| Vue | latest |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 12 (6 SFCs) |

## Original skeleton

- Archetype: **terminal-console** (linear)
- Traits: hero, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 15
- Top-level tags: div, svg, header, nav, footer, div

The replacement skeleton must not be `terminal-console` and must not be in the same family (`linear`).

## Routes

- `/`

## Palette (most used first)

`#ff0000` (29) · `#000000` (19) · `#8fa3b5` (19) · `#182533` (12) · `#111a24` (9) · `#05080c` (5) · `#5ce1a0` (5) · `#0c131c` (4) · `#f2c94c` (4) · `#ff00ff` (4)

## Content lock

- Static visible text tokens: **246**
- Binding expressions: **152**
- Event handlers: **50**
- Contract hash: `87df55a4fd458048fee4007ca6ab08175339b2d0c3d47b67a74e909b4ffd75f0`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/703/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/703/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
