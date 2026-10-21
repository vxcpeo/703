"""Build src/styles/bubblegum.css from the previous skin.

Renames every .ax-* selector to .bg-*, swaps the token layer for the selected
Bubblegum Exchange palette, converts the dark-surface literals to the light
surface family, and appends the Split Stage shell rules.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"E:\workspace\chuangye\solana\703\website")
SRC = ROOT / "src" / "styles" / "reskin.css"
DST = ROOT / "src" / "styles" / "bubblegum.css"

TOKENS = """:root {
  --bg: #ffffff;
  --surface: #f9f8fa;
  --surface-alt: #f2eef3;
  --ink: #0d0d0d;
  --muted: #6d6a70;
  --accent: #e6006f;
  --accent-safe: #c2005d;
  --accent-2: #ff4da6;
  --line: #e9e4eb;
  --success: #0f7b4d;
  --danger: #b02323;
  --warning: #7a4e00;
  --signal: #c2005d;

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
  --glow: 0 0 0 1px rgba(230, 0, 111, 0.18), 0 18px 40px rgba(230, 0, 111, 0.1);

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
  --rail: 0px;
}
"""

# Ordered, longest-first literal replacement table for the old dark skin.
COLOR_MAP = [
    ("rgba(255, 255, 255,", "rgba(13, 13, 13,"),
    ("rgba(143, 163, 181,", "rgba(109, 106, 112,"),
    ("rgba(255, 0, 0,", "rgba(230, 0, 111,"),
    ("rgba(255, 0, 255,", "rgba(255, 77, 166,"),
    ("rgba(17, 26, 36,", "rgba(249, 248, 250,"),
    ("rgba(24, 37, 51,", "rgba(242, 238, 243,"),
    ("rgba(9, 14, 20,", "rgba(255, 255, 255,"),
    ("rgba(10, 15, 22,", "rgba(255, 255, 255,"),
    ("rgba(11, 17, 26,", "rgba(255, 255, 255,"),
    ("rgba(0, 0, 0, 0.55)", "rgba(20, 10, 25, 0.28)"),
    ("rgba(0, 0, 0, 0.6)", "rgba(20, 10, 25, 0.3)"),
    ("rgba(0, 0, 0, 0.5)", "rgba(20, 10, 25, 0.22)"),
    ("rgba(0, 120, 160,", "rgba(255, 77, 166,"),
    ("#05080c", "var(--surface)"),
    ("#0c131c", "var(--surface)"),
    ("#0b111a", "var(--surface)"),
    ("#0a1017", "var(--surface)"),
    ("#0d1420", "var(--surface)"),
    ("#101a24", "var(--surface)"),
    ("#111a24", "var(--surface)"),
    ("#182533", "var(--surface-alt)"),
    ("#1e2a36", "var(--line)"),
    ("#f4f7fa", "var(--ink)"),
    ("#8fa3b5", "var(--muted)"),
    ("#a9bbcb", "var(--muted)"),
    ("#40698c", "var(--accent-safe)"),
    ("#2a4a63", "var(--surface-alt)"),
    ("#ff2f2f", "var(--accent)"),
    ("#ff8bff", "var(--accent-2)"),
    ("#ff6b6b", "var(--danger)"),
    ("#ff0000", "var(--accent)"),
    ("#ff00ff", "var(--accent-2)"),
    ("#5ce1a0", "var(--success)"),
    ("#ff7a7a", "var(--danger)"),
    ("#f2c94c", "var(--warning)"),
    ("rgba(242, 201, 76,", "rgba(138, 90, 0,"),
]

text = SRC.read_text(encoding="utf-8")

# 1. drop the old token block
start = text.index(":root {")
end = text.index("}", start) + 1
body = text[:start] + text[end:]

# 2. rename classes / keyframes that carry the old namespace
body = body.replace(".ax-", ".bg-")
body = body.replace("ax-spin", "bg-spin")
body = body.replace("name=\"page\"", "name=\"page\"")

# 3. retheme literals
for old, new in COLOR_MAP:
    body = body.replace(old, new)

# 4. text on accent fills must be white
body = body.replace("color: #000;", "color: #ffffff;")
body = body.replace("color: #000000;", "color: #ffffff;")
body = body.replace("color: #fff;", "color: #ffffff;")

# 5. drop the old shell sections: they are replaced by the Split Stage block.
def cut(pattern: str) -> None:
    global body
    match = re.search(pattern, body)
    if match:
        body = body[: match.start()] + body[match.end() :]


# The old shell rules live between the base reset and the component grammar.
cut(r"/\* -+ shell -+ \*/")
cut(r"/\* -+ rail -+ \*/")
cut(r"/\* -+ command -+ \*/")
# remove the leftover shell blocks that follow the component grammar
for marker in (
    r"/\* -+ status strip -+ \*/",
    r"/\* -+ drawer -+ \*/",
):
    cut(marker)

body = body.replace("/* -+", "/*")

SHELL = r"""
/* ==========================================================================
   Split Stage shell — sticky narrative column + scrolling evidence stage
   ========================================================================== */

.bg-frame {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(300px, 38fr) minmax(0, 62fr);
  align-items: start;
  min-height: 100vh;
  background: var(--bg);
}

.bg-skip {
  position: fixed;
  top: 10px;
  inset-inline-start: 12px;
  z-index: 90;
  padding: 10px 18px;
  border-radius: 999px;
  background: var(--ink);
  color: #ffffff;
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-decoration: none;
  clip-path: inset(50%);
}

.bg-skip:focus-visible {
  clip-path: inset(0 0 0 0);
}

.bg-narrative {
  position: sticky;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: clamp(20px, 3vw, 44px);
  height: 100vh;
  max-height: 100vh;
  overflow-y: auto;
  padding: clamp(22px, 3.4vw, 52px) clamp(20px, 3vw, 48px);
  background:
    radial-gradient(70% 52% at 12% 4%, rgba(255, 77, 166, 0.16), transparent 68%),
    radial-gradient(58% 46% at 96% 100%, rgba(230, 0, 111, 0.12), transparent 70%),
    var(--surface);
  border-inline-end: 1px solid var(--line);
  scrollbar-width: thin;
}

.bg-current {
  min-height: 100vh;
  padding: clamp(28px, 4vw, 64px) clamp(20px, 4.6vw, 76px) clamp(56px, 6vw, 96px);
  background: var(--bg);
}

.bg-current:focus-visible {
  outline-offset: -6px;
}

/* --- narrative index ---------------------------------------------------- */

.bg-index {
  display: flex;
  flex-direction: column;
  gap: clamp(16px, 2.4vw, 28px);
}

.bg-brandline {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0;
  color: var(--ink);
  text-decoration: none;
}

.bg-brandline-mark {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: var(--bg);
  border: 1px solid var(--line);
  box-shadow: 0 10px 24px rgba(20, 10, 25, 0.08);
  overflow: hidden;
}

.bg-brandline-mark img {
  width: 40px;
  height: 40px;
}

.bg-brandline-text {
  display: grid;
  gap: 2px;
}

.bg-brandline-word {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 21px;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.bg-brandline-accent {
  color: var(--accent-safe);
}

.bg-brandline-tag {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
}

.bg-index-list {
  counter-reset: bg-index;
  display: grid;
  gap: 2px;
  border-top: 1px solid var(--line);
  padding-top: 10px;
}

.bg-index-list > li {
  counter-increment: bg-index;
}

.bg-index-link {
  display: grid;
  grid-template-columns: 26px 20px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 11px 8px;
  border-radius: 14px;
  color: var(--ink);
  text-decoration: none;
  border: 1px solid transparent;
  transition: background var(--motion-duration) var(--motion-ease),
    border-color var(--motion-duration) var(--motion-ease);
}

.bg-index-link::before {
  content: counter(bg-index, decimal-leading-zero);
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.bg-index-link:hover {
  background: var(--bg);
  border-color: var(--line);
}

.bg-index-link[aria-current="page"] {
  background: var(--bg);
  border-color: var(--accent);
  box-shadow: 0 8px 22px rgba(230, 0, 111, 0.1);
}

.bg-index-link[aria-current="page"]::before {
  color: var(--accent-safe);
}

.bg-index-glyph {
  display: inline-grid;
  place-items: center;
  color: var(--accent-safe);
}

.bg-index-label {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.bg-index-badge {
  min-width: 22px;
  padding: 2px 7px;
  border-radius: 999px;
  background: var(--surface-alt);
  border: 1px solid var(--line);
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--ink);
  text-align: center;
}

.bg-index-rule {
  display: block;
  height: 1px;
  background: linear-gradient(90deg, var(--line), transparent);
}

/* --- narrative console -------------------------------------------------- */

.bg-console {
  display: grid;
  gap: 12px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--bg);
  box-shadow: 0 16px 36px rgba(20, 10, 25, 0.06);
}

.bg-console-top {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bg-console-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 10px;
  border-radius: 999px;
  background: var(--surface-alt);
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink);
}

.bg-console-pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(230, 0, 111, 0.16);
}

.bg-console-rule {
  flex: 1;
  height: 1px;
  background: var(--line);
}

.bg-console-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bg-console-icon {
  display: inline-grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: var(--surface);
  color: var(--ink);
  transition: border-color var(--motion-duration) var(--motion-ease),
    background var(--motion-duration) var(--motion-ease);
}

.bg-console-icon:hover {
  border-color: var(--accent);
  background: var(--bg);
}

.bg-console-icon:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.bg-spin {
  animation: bg-turn 900ms linear infinite;
}

@keyframes bg-turn {
  to {
    transform: rotate(360deg);
  }
}

/* --- narrative colophon ------------------------------------------------- */

.bg-colophon {
  display: grid;
  gap: 16px;
  padding-top: 18px;
  border-top: 1px solid var(--line);
  font-size: 12px;
  color: var(--muted);
}

.bg-colophon-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bg-colophon-mark img {
  width: 24px;
  height: 24px;
}

.bg-colophon-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--ink);
}

.bg-colophon-name .bg-colophon-accent {
  color: var(--accent-safe);
}

.bg-colophon-tag {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.bg-colophon-note {
  font-size: 12px;
  line-height: 1.6;
  color: var(--muted);
}

.bg-colophon-links {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 14px;
}

.bg-colophon-links button {
  padding: 0;
  font-size: 12px;
  color: var(--ink);
  text-decoration: underline;
  text-decoration-color: var(--line);
  text-underline-offset: 3px;
}

.bg-colophon-links button:hover {
  color: var(--accent-safe);
}

.bg-colophon-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 16px;
  font-size: 11.5px;
}

.bg-colophon-facts span {
  display: grid;
  gap: 1px;
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}

.bg-colophon-facts b {
  font-family: var(--font-body);
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
  color: var(--ink);
}

.bg-colophon-word {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(38px, 6vw, 62px);
  line-height: 0.9;
  letter-spacing: -0.04em;
  color: var(--surface-alt);
}

.bg-colophon-word .bg-colophon-word-accent {
  color: rgba(230, 0, 111, 0.35);
}

.bg-colophon-fine {
  display: grid;
  gap: 2px;
  font-size: 11px;
  color: var(--muted);
  border-top: 1px solid var(--line);
  padding-top: 10px;
}

/* --- drawer / overlay --------------------------------------------------- */

.bg-veil {
  position: fixed;
  inset: 0;
  z-index: 60;
  background: rgba(20, 10, 25, 0.32);
  backdrop-filter: blur(3px);
}

.bg-drawer {
  position: fixed;
  inset-block: 0;
  inset-inline-end: 0;
  z-index: 70;
  display: flex;
  flex-direction: column;
  gap: 18px;
  width: min(380px, 88vw);
  padding: 22px;
  background: var(--bg);
  border-inline-start: 1px solid var(--line);
  box-shadow: -24px 0 60px rgba(20, 10, 25, 0.16);
  overflow-y: auto;
}

.bg-drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bg-drawer-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 18px;
}

.bg-drawer-nav {
  display: grid;
  gap: 4px;
}

.bg-drawer-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 10px;
  border-radius: 14px;
  border: 1px solid transparent;
  color: var(--ink);
  font-size: 14px;
  text-align: start;
}

.bg-drawer-link:hover {
  background: var(--surface);
  border-color: var(--line);
}

.bg-drawer-link b {
  margin-inline-start: auto;
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--muted);
}

.bg-drawer-foot {
  margin-top: auto;
  display: grid;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--line);
}

.bg-drawer-facts {
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: var(--muted);
}

.bg-drawer-facts span {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.bg-drawer-facts b {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink);
}

/* --- stage body --------------------------------------------------------- */

.bg-current .bg-alerts {
  max-width: 1080px;
  margin-inline: auto;
}

.bg-current .bg-view {
  max-width: 1080px;
  margin-inline: auto;
}

/* --- mobile ------------------------------------------------------------- */

@media (max-width: 1023px) {
  .bg-frame {
    grid-template-columns: minmax(0, 1fr);
  }

  .bg-narrative {
    position: static;
    height: auto;
    max-height: none;
    overflow: visible;
    border-inline-end: 0;
    border-block-end: 1px solid var(--line);
    gap: 18px;
    padding: 20px 18px 22px;
  }

  .bg-index-list {
    grid-auto-flow: column;
    grid-auto-columns: minmax(132px, max-content);
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 6px;
    scrollbar-width: thin;
  }

  .bg-index-link {
    grid-template-columns: 18px 18px minmax(0, 1fr) auto;
    padding: 9px 10px;
    background: var(--bg);
    border-color: var(--line);
  }

  .bg-console {
    grid-template-columns: minmax(0, 1fr);
  }

  .bg-current {
    padding: 24px 18px 56px;
  }

  .bg-colophon-word {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .bg-spin {
    animation: none;
  }

  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
"""

header = """/* ==========================================================================
   Clepsyra — Bubblegum Exchange / Split Stage
   Light fintech surface, single magenta accent, mono micro-labels.
   Namespace: bg-
   ========================================================================== */

"""

DST.write_text(header + TOKENS + body + SHELL, encoding="utf-8")
print(f"wrote {DST} ({len((header + TOKENS + body + SHELL).splitlines())} lines)")
