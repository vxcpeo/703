# Reskin inventory — attesio-web

Generated: 2026-10-19T18:49:04.322Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/703/website` |
| Vue | latest |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 11 (5 SFCs) |

## Original skeleton

- Archetype: **dashboard-shell** (shell)
- Traits: sidebar, topbar, cards, hero, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 15
- Top-level tags: div, svg, footer, header, div

The replacement skeleton must not be `dashboard-shell` and must not be in the same family (`shell`).

## Routes

- `/`

## Palette (most used first)

`#fffdf8` (14) · `#b1741a` (6) · `#e7ddcb` (6) · `#1c1710` (3) · `#0c3428` (2) · `#0d382c` (2) · `#14503f` (2) · `#18130d` (2) · `#2c5568` (2) · `#8b3a32` (2)

## Content lock

- Static visible text tokens: **246**
- Binding expressions: **148**
- Event handlers: **50**
- Contract hash: `b4c3e407879d7c9afa3a8e27bae2c8333c3e29c09d945bbefd35944126062eee`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/703/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/703/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
