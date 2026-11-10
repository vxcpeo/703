# Reskin verification — PASS

Generated: 2026-11-09T18:14:25.016Z

- Project: **docketa-web**
- URL: http://127.0.0.1:4318/
- Original skeleton: `sidebar-workspace` (shell)
- New skeleton: `orbital` (spatial)
- Accent: #e6006f -> #ff0000 (61.43 ΔE; min 30)
- Source contract: intact (`ce9228ec8b28`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.455 | 0.333 | 0 | [desktop](current/home-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: numeric token count changed: 14 -> 12 (dynamic values may differ)

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
