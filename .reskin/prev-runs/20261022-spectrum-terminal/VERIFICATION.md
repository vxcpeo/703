# Reskin verification — PASS

Generated: 2026-10-21T14:00:20.009Z

- Project: **actoria-web**
- URL: http://127.0.0.1:4317/
- Original skeleton: `sidebar-workspace` (shell)
- New skeleton: `terminal-console` (linear)
- Accent: #e6006f -> #9945ff (85.01 ΔE; min 30)
- Source contract: intact (`2cd00ec31667`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.375 | 0.3 | 0 | [desktop](current/home-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: aria attribute added: aria-label=Marginal notes
- /: aria attribute added: aria-label=Record bands

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
