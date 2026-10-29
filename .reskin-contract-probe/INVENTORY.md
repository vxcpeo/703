# Reskin inventory — rationum-web

Generated: 2026-10-22T15:23:39.462Z

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

- Archetype: **sidebar-workspace** (shell)
- Traits: sidebar, cards, hero, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 17
- Top-level tags: div, svg, div, a, footer, nav, div

The replacement skeleton must not be `sidebar-workspace` and must not be in the same family (`shell`).

## Routes

- `/`

## Palette (most used first)

`#ffffff` (30) · `#e6006f` (5) · `#c42b2b` (4) · `#0d0d0d` (3) · `#0f7b4d` (3) · `#8a5a00` (3) · `#ff4da6` (3) · `#fff8e8` (2) · `#35313a` (1) · `#6d6a70` (1)

## Content lock

- Static visible text tokens: **245**
- Binding expressions: **153**
- Event handlers: **50**
- Contract hash: `ca0d7a808a8baeb46b7db4c18b13126c6833b9ea3fff46101f58dde4d4c40ad3`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/703/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/703/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
