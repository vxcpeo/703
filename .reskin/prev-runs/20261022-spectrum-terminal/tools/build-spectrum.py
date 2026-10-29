#!/usr/bin/env python3
"""Rebuild App.vue's template into the Spectrum Terminal (ticker-stage) skeleton.

The script keeps the <script setup> block byte-for-byte and only restructures
markup: the split-stage aside becomes a masthead + ticker + status footer, the
two-column stage becomes a stack of full-width bands, wrapper tags are replaced
and each band gains an inner wrapper (new DOM depth). Every binding, handler,
attribute and text node is preserved.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
APP = ROOT / "src" / "App.vue"
OUT = ROOT / ".reskin" / "logs"
OUT.mkdir(parents=True, exist_ok=True)

source = APP.read_text(encoding="utf-8")
script_end = source.index("</script>") + len("</script>")
script = source[:script_end]
template_start = source.index("<template>") + len("<template>")
template = source[template_start : source.rindex("</template>")]

report: dict[str, list] = {"steps": []}


def step(name: str, detail: str = "") -> None:
    report["steps"].append({"name": name, "detail": detail})


def match_element(html: str, pattern: str, tag: str, from_pos: int = 0) -> tuple[int, int, int, int] | None:
    m = re.compile(pattern, re.S).search(html, from_pos)
    if not m:
        return None
    open_start = m.start()
    open_end = html.index(">", m.start()) + 1
    depth = 1
    pos = open_end
    open_re = re.compile(rf"<{tag}\b[^>]*?(/?)>", re.S)
    close_re = re.compile(rf"</{tag}\s*>")
    while depth:
        nxt_open = open_re.search(html, pos)
        nxt_close = close_re.search(html, pos)
        if not nxt_close:
            raise SystemExit(f"unbalanced <{tag}> for {pattern}")
        if nxt_open and nxt_open.start() < nxt_close.start():
            if not nxt_open.group(1):
                depth += 1
            pos = nxt_open.end()
        else:
            depth -= 1
            pos = nxt_close.end()
            if depth == 0:
                return open_start, open_end, nxt_close.start(), nxt_close.end()
    return None


def retag_all(html: str, pattern: str, old_tag: str, new_open: str, new_tag: str) -> tuple[str, int]:
    count = 0
    pos = 0
    while True:
        found = match_element(html, pattern, old_tag, pos)
        if not found:
            break
        open_start, open_end, close_start, close_end = found
        replacement = new_open if callable(new_open) is False else new_open(html[open_start:open_end])
        html = html[:open_start] + replacement + html[open_end:close_start] + f"</{new_tag}>" + html[close_end:]
        pos = open_start + len(replacement)
        count += 1
    return html, count


def wrap_all(html: str, pattern: str, tag: str, wrapper: str) -> tuple[str, int]:
    positions = []
    pos = 0
    while True:
        found = match_element(html, pattern, tag, pos)
        if not found:
            break
        positions.append(found)
        pos = found[0] + 1
    count = 0
    for open_start, open_end, close_start, close_end in reversed(positions):
        inner = html[open_end:close_start]
        if f'<div class="{wrapper}">' in inner[:200]:
            continue
        html = html[:open_end] + f'\n        <div class="{wrapper}">' + inner + "\n        </div>" + html[close_start:]
        count += 1
    return html, count


# --- 1. Class namespace and structural renames ----------------------------
template, renamed = re.subn(r"\bbg-", "sp-", template)
step("rename", f"{renamed} bg- tokens renamed to sp-")

families = [
    ("sp-tags", "sp-filterstrip"),
    ("sp-tag--strong", "sp-filtertab--strong"),
    ("sp-tag", "sp-filtertab"),
    ("sp-board", "sp-band"),
    ("sp-sheet", "sp-slab"),
    ("sp-readout", "sp-dial"),
    ("sp-fork", "sp-door"),
    ("sp-wide", "sp-flow"),
    ("sp-margin", "sp-tail"),
    ("sp-stage", "sp-bands"),
    ("sp-runhead", "sp-statement"),
    ("sp-btn--fill", "sp-btn--solid"),
    ("sp-command-icon", "sp-icon-btn"),
    ("sp-frame", "sp-shell"),
    ("sp-current", "sp-main"),
    ("sp-view", "sp-route"),
    ("sp-alerts", "sp-notices"),
    ("sp-alert", "sp-notice"),
    ("sp-display", "sp-headline"),
    ("sp-lede", "sp-deck"),
    ("sp-kicker", "sp-eyebrow"),
]
for old, new in families:
    template, n = re.subn(rf"\b{re.escape(old)}", new, template)
    if n:
        step("family", f"{old} -> {new} ({n})")

# --- 2. Shell -------------------------------------------------------------
aside = match_element(template, r'<aside class="sp-narrative">', "aside")
if not aside:
    raise SystemExit("narrative aside not found")
a_start, a_end, a_close_start, a_close_end = aside
masthead = """<header class="sp-masthead">
      <RailNav :tabs="navTabs" :active="route" @navigate="navigate" />

      <CommandBar
        :cluster="SOLANA_CLUSTER"
        :wallet-label="walletLabel"
        :connected="connected"
        :reading="reading"
        :busy="busy"
        :connecting="connecting"
        :menu-open="menuOpen"
        @sync="refresh"
        @wallet="connected ? disconnectWallet() : connect()"
        @menu="toggleMenu"
      />
    </header>

    <TickerNav :tabs="navTabs" :active="route" @navigate="navigate" />"""
template = template[:a_start] + masthead + template[a_close_end:]
step("shell", "split-stage aside replaced by masthead + ticker")

drawer = match_element(template, r'<template v-if="menuOpen">', "template")
if not drawer:
    raise SystemExit("drawer template not found")
d_start, d_end, dc_start, dc_end = drawer
old_drawer = template[d_start:dc_end]
template = template[:d_start] + template[dc_end:]
step("shell", "drawer lifted out of the frame")

status_strip = """<StatusStrip
      :tabs="navTabs"
      :network-name="SOLANA_NETWORK_NAME"
      :cluster="SOLANA_CLUSTER"
      :program-state="programState"
      :mint-state="mintState"
      :wallet-label="walletLabel"
      :last-read="lastRead || 'Not yet'"
      @navigate="navigate"
    />"""
main_close = template.index("</main>")
template = (
    template[:main_close]
    + "</main>\n\n    "
    + status_strip
    + "\n\n    "
    + old_drawer
    + template[main_close + len("</main>") :]
)
step("shell", "status footer and drawer placed after main")

# --- 3. Wrapper tags and inner band depth ---------------------------------
template, n = retag_all(template, r'<div class="sp-statement">', "div", '<header class="sp-statement">', "header")
step("tag", f"statement header ({n})")
template, n = wrap_all(template, r'<header class="sp-statement">', "header", "sp-statement-inner")
step("wrap", f"statement inner ({n})")

template, n = retag_all(template, r'<div class="sp-bands">', "div", '<section class="sp-bands" aria-label="Record bands">', "section")
step("tag", f"bands section ({n})")
template, n = retag_all(template, r'<div class="sp-flow">', "div", '<div class="sp-flow">', "div")
step("tag", f"flow ({n})")
template, n = retag_all(template, r'<div class="sp-tail">', "div", '<section class="sp-tail" aria-label="Marginal notes">', "section")
step("tag", f"tail section ({n})")

template, n = retag_all(template, r'<section class="sp-band(?:--loading)?">', "section", '<article class="sp-band">', "article")
step("tag", f"board -> article band ({n})")
template, n = wrap_all(template, r'<article class="sp-band">', "article", "sp-band-inner")
step("wrap", f"band inner ({n})")

template, n = retag_all(template, r'<div class="sp-band-head">', "div", '<header class="sp-band-head">', "header")
step("tag", f"band head header ({n})")

template, n = retag_all(template, r'<div class="sp-slab">', "div", '<section class="sp-slab">', "section")
step("tag", f"slab section ({n})")
template, n = wrap_all(template, r'<section class="sp-slab">', "section", "sp-slab-inner")
step("wrap", f"slab inner ({n})")
template, n = retag_all(template, r'<div class="sp-slab-head">', "div", '<header class="sp-slab-head">', "header")
step("tag", f"slab head header ({n})")

for cls in ("sp-ledger", "sp-checklist", "sp-steps"):
    template, n = retag_all(template, rf'<ul class="{cls}">', "ul", f'<ol class="{cls}">', "ol")
    step("tag", f"{cls} list -> ordered list ({n})")

template, n = retag_all(template, r'<section class="sp-dial"', "section", '<section class="sp-dials" aria-label="Live readouts">', "section")
step("tag", f"dials section ({n})")
template, n = retag_all(template, r'<div class="sp-dial-grid">', "div", '<div class="sp-beats">', "div")
step("tag", f"beats row ({n})")
template, n = retag_all(template, r'<div class="sp-dial-cell">', "div", '<div class="sp-beat">', "div")
step("tag", f"beat cells ({n})")
template, n = retag_all(template, r'<section class="sp-doors"', "section", '<section class="sp-doors" aria-label="Ways to take part">', "section")
step("tag", f"doors section ({n})")

# --- 4. Install TickerNav import ------------------------------------------
if "TickerNav" not in script:
    lines = script.splitlines()
    inserted = False
    for i, line in enumerate(lines):
        if line.startswith("import ") and "from " in line:
            lines.insert(i + 1, 'import TickerNav from "./components/TickerNav.vue";')
            inserted = True
            break
    if not inserted:
        lines.insert(0, 'import TickerNav from "./components/TickerNav.vue";')
    script = "\n".join(lines)
    step("script", "TickerNav import inserted")

new_source = script + "\n\n<template>" + template + "</template>\n"
APP.write_text(new_source, encoding="utf-8")
(OUT / "build-spectrum.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"ok": True, "steps": len(report["steps"]), "app": str(APP), "bytes": len(new_source)}, indent=2))
