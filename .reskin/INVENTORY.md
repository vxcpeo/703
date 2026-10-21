# Reskin inventory — actoria-web

Generated: 2026-10-21T13:44:48.944Z

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

- Archetype: **sidebar-workspace** (shell)
- Traits: sidebar, hero, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 14
- Top-level tags: div, svg, div, nav, footer, div

The replacement skeleton must not be `sidebar-workspace` and must not be in the same family (`shell`).

## Routes

- `/`

## Palette (most used first)

`#e6006f` (27) · `#f9f8fa` (25) · `#6d6a70` (18) · `#ffffff` (16) · `#f2eef3` (12) · `#5ce1a0` (4) · `#ff4da6` (4) · `#140a19` (3) · `#8a5a00` (3) · `#000000` (2)

## Content lock

- Static visible text tokens: **246**
- Binding expressions: **152**
- Event handlers: **50**
- Contract hash: `2cd00ec31667df958c64f010a822864c4aa97ac816e8a9ae39910dee437f7dbb`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/703/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/703/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
