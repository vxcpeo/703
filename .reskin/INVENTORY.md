# Reskin inventory — rationum-web

Generated: 2026-10-22T15:10:15.999Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/703/website` |
| Vue | latest |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 13 (7 SFCs) |

## Original skeleton

- Archetype: **terminal-console** (linear)
- Traits: hero, grid, tabs, modal, charts, sticky, terminal, ticker
- Max template depth: 15
- Top-level tags: div, svg, div, div, footer, nav, div

The replacement skeleton must not be `terminal-console` and must not be in the same family (`linear`).

## Routes

- `/`

## Palette (most used first)

`#000000` (8) · `#14f195` (5) · `#9945ff` (4) · `#ffffff` (3) · `#050506` (2) · `#0b0b0c` (2) · `#161618` (1) · `#1b1b1e` (1) · `#29292d` (1) · `#a6a6aa` (1)

## Content lock

- Static visible text tokens: **246**
- Binding expressions: **152**
- Event handlers: **50**
- Contract hash: `12761c50ee087292510e1c948499eb0f8beb36a25712d9d0e44868ae35ec88da`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/703/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/703/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
