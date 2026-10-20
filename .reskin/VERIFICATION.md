# Reskin verification — PASS

Generated: 2026-10-19T19:05:47.582Z

- Project: **attesio-web**
- URL: http://127.0.0.1:4319/
- Original skeleton: `dashboard-shell` (shell)
- New skeleton: `terminal-console` (linear)
- Accent: #b1741a -> #ff0000 (64.32 ΔE; min 30)
- Source contract: intact (`652f1c8d5c37`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.449 | 0.455 | 0 | [desktop](current/home-desktop.png) |

## Blocking issues

- None.

## Warnings

- bindings: added "attr:'#' + tab.id"
- bindings: added "attr:'#home'"
- bindings: added "link:'#' + tab.id"
- bindings: added "link:'#home'"
- /: aria attribute added: aria-label=Open menu
- /: link target added: #governance
- /: link target added: #home
- /: link target added: #learn
- /: link target added: #quests
- /: link target added: #stake
- /: link target added: #treasury

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
