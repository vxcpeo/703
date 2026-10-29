#!/usr/bin/env python3
"""Rebuild App.vue's template into the Split Stage skeleton (Bubblegum Exchange).

The <script setup> block is copied byte-for-byte. The template is transformed:
every route keeps its exact content tokens, but the statement header is moved
into a sticky narrative column and the data bodies are re-wrapped for the
scrolling stage. Class names are remapped to the new token namespace.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\workspace\chuangye\solana\703\website")
APP = ROOT / "src" / "App.vue"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from class_map import MAP  # noqa: E402


def rename_classes(text: str) -> str:
    def repl(match: re.Match) -> str:
        tokens = match.group(1).split()
        return 'class="' + " ".join(MAP.get(token, token) for token in tokens) + '"'

    def repl_expr(match: re.Match) -> str:
        expr = match.group(1)
        for old, new in MAP.items():
            expr = expr.replace(f"'{old}'", f"'{new}'")
        return ':class="' + expr + '"'

    text = re.sub(r'class="([^"]*)"', repl, text)
    text = re.sub(r':class="([^"]*)"', repl_expr, text)
    return text


def find_matching(text: str, start: int, tag: str) -> int:
    open_re = re.compile(rf"<{tag}\b")
    close_re = re.compile(rf"</{tag}>")
    depth = 0
    i = start
    while i < len(text):
        o = open_re.search(text, i)
        c = close_re.search(text, i)
        if not o and not c:
            raise SystemExit(f"unbalanced {tag}")
        if c and (not o or c.start() < o.start()):
            depth -= 1
            if depth == 0:
                return c.start() + len(c.group(0))
            i = c.end()
        else:
            depth += 1
            i = o.end()
    raise SystemExit(f"unclosed {tag}")


PART_RE = {
    "eyebrow": re.compile(r'<p class="sp-eyebrow">.*?</p>', re.S),
    "headline": re.compile(r'<h1[^>]*class="sp-headline"[^>]*>.*?</h1>', re.S),
    "deck": re.compile(r'<p class="sp-deck">.*?</p>', re.S),
    "actions": re.compile(r'<div class="sp-actions">.*?</div>\s*\n', re.S),
    "facts": re.compile(r'<ul class="sp-facts">.*?</ul>', re.S),
    "filterstrip": re.compile(r'<div class="sp-filterstrip">.*?</div>\s*\n', re.S),
}


def split_statement(inner: str) -> tuple[str, str]:
    start = inner.find('<header class="sp-statement">')
    if start < 0:
        raise SystemExit("no statement header")
    end = inner.find("</div></header>", start) + len("</div></header>")
    return inner[start:end], inner[:start] + inner[end:]


def parse_statement(statement: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    for key, pattern in PART_RE.items():
        m = pattern.search(statement)
        if m:
            parts[key] = m.group(0).strip()
    return parts


def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in text.splitlines())


def main() -> int:
    source = APP.read_text(encoding="utf-8")
    script_end = source.find("</script>") + len("</script>")
    script = source[:script_end]
    template = source[script_end:]

    route_section_start = template.find('<section :key="route" class="sp-route">')
    route_inner_start = template.find(">", route_section_start) + 1
    m_close = re.search(r"</section>\n\s*</Transition>", template[route_inner_start:])
    routes_text = template[route_inner_start:route_inner_start + m_close.start()]

    comments = list(re.finditer(r"<!-- =+ (\w+) ==== -->", routes_text))
    if len(comments) != 6:
        raise SystemExit(f"expected 6 route comments, found {len(comments)}")

    thesis_blocks = []
    body_blocks = []
    for idx, comment in enumerate(comments):
        block_start = routes_text.find("<template", comment.end())
        open_end = routes_text.find(">", block_start) + 1
        open_tag = routes_text[block_start:open_end]
        name_match = re.search(r"route === ['\"](\w+)['\"]", open_tag)
        if not name_match:
            raise SystemExit(f"unexpected route block: {open_tag}")
        name = name_match.group(1)
        block_end = find_matching(routes_text, block_start, "template")
        inner = routes_text[open_end:block_end - len("</template>")]
        statement, body = split_statement(inner)
        parts = parse_statement(statement)
        for required in ("eyebrow", "headline", "deck"):
            if required not in parts:
                raise SystemExit(f"{name}: missing {required}")
        order = [parts["eyebrow"], parts["headline"], parts["deck"]]
        for extra in ("filterstrip", "actions", "facts"):
            if extra in parts:
                order.append(parts[extra])
        thesis = rename_classes("\n".join(order))
        thesis_blocks.append(
            f"        <template v-if=\"route === '{name}'\">\n"
            f"          <div class=\"bz-thesis\">\n{indent(thesis, 12)}\n          </div>\n"
            f"        </template>"
        )
        body = rename_classes(body.strip("\n"))
        body_blocks.append(
            f"            <template v-if=\"route === '{name}'\">\n"
            f"              <div class=\"bz-sheet\">\n{indent(body, 16)}\n              </div>\n"
            f"            </template>"
        )

    notices_start = template.find('<div class="sp-notices">')
    notices_end = template.find("</div>\n\n      <Transition", notices_start) + len("</div>")
    notices = rename_classes(template[notices_start:notices_end])

    shell = """<template>
  <div class="bz-app">
    <a class="bz-skip" href="#main" @click.prevent="focusMain">Skip to content</a>

    <div class="bz-frame">
      <aside class="bz-rail">
        <RailNav />

        <TickerNav :tabs="navTabs" :active="route" @navigate="navigate" />

        <div class="bz-rail-thesis">
__THESIS__
        </div>

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

        <StatusStrip
          :tabs="navTabs"
          :network-name="SOLANA_NETWORK_NAME"
          :cluster="SOLANA_CLUSTER"
          :program-state="programState"
          :mint-state="mintState"
          :wallet-label="walletLabel"
          :last-read="lastRead || 'Not yet'"
          @navigate="navigate"
        />
      </aside>

      <main id="main" class="bz-stage" tabindex="-1">
__NOTICES__

        <Transition name="bz-swap" mode="out-in">
          <section :key="route" class="bz-view">
__BODIES__
          </section>
        </Transition>
      </main>
    </div>

    <template v-if="menuOpen">
      <div class="bz-veil" @click="menuOpen = false"></div>
      <div id="ax-drawer" class="bz-drawer" aria-label="Sections and wallet" role="complementary">
        <header class="bz-drawer-head">
          <span class="bz-drawer-title">Rationum</span>
          <button class="bz-icon-btn" type="button" aria-label="Close menu" @click="menuOpen = false">
            <Icon name="close" :size="18" />
          </button>
        </header>
        <nav class="bz-drawer-nav" aria-label="Sections">
          <button
            v-for="tab in navTabs"
            :key="tab.id"
            class="bz-drawer-link"
            type="button"
            :aria-current="route === tab.id ? 'page' : undefined"
            @click="navigate(tab.id)"
          >
            <Icon :name="tab.icon" :size="18" />
            <span>{{ tab.label }}</span>
            <b v-if="tab.badge !== null && tab.badge !== undefined">{{ tab.badge }}</b>
          </button>
        </nav>
        <div class="bz-drawer-foot">
          <button
            class="bz-btn bz-btn--fill bz-btn--wide"
            type="button"
            :disabled="connecting || busy"
            @click="connected ? disconnectWallet() : connect()"
          >
            <Icon name="wallet" :size="16" />
            {{ connected ? "Disconnect wallet" : "Connect wallet" }}
          </button>
          <div class="bz-drawer-facts">
            <span>Cluster <b>{{ SOLANA_CLUSTER }}</b></span>
            <span>Program <b>{{ programState }}</b></span>
            <span>Wallet <b>{{ walletLabel }}</b></span>
          </div>
        </div>
      </div>
    </template>

    <div
      v-if="txState.stage !== 'idle'"
      class="bz-toast"
      :data-tone="txState.stage === 'error' ? 'error' : txState.stage === 'success' ? 'success' : 'idle'"
      :role="txState.stage === 'error' ? 'alert' : 'status'"
      aria-live="polite"
      aria-atomic="true"
    >
      <span class="bz-toast-dot" aria-hidden="true"></span>
      <div class="bz-toast-copy">
        <strong>{{ txState.label }}</strong>
        <p>{{ txState.message }}</p>
        <a
          v-if="txState.hash"
          :href="explorer('tx', txState.hash)"
          target="_blank"
          rel="noopener noreferrer"
        >View transaction <Icon name="arrow-up-right" :size="13" /></a>
      </div>
      <button
        v-if="!busy"
        class="bz-icon-btn bz-toast-close"
        type="button"
        aria-label="Dismiss transaction status"
        @click="dismissToast"
      >
        <Icon name="close" :size="16" />
      </button>
    </div>

    <WalletSheet
      v-if="walletPickerOpen"
      :options="walletOptions"
      :network-name="SOLANA_NETWORK_NAME"
      @choose="chooseWallet"
      @close="closeWalletPicker"
    />
  </div>
</template>
"""
    new_template = (shell
                    .replace("__THESIS__", "\n".join(thesis_blocks))
                    .replace("__NOTICES__", indent(notices, 8))
                    .replace("__BODIES__", "\n".join(body_blocks)))

    output = script + "\n\n" + new_template
    backup = ROOT.parent / ".rebrand" / "reskin-backup"
    backup.mkdir(parents=True, exist_ok=True)
    (backup / "App.vue.before").write_text(source, encoding="utf-8")
    APP.write_text(output, encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "scriptUnchanged": source[:script_end] == output[:script_end],
        "routes": [c.group(1).lower() for c in comments],
        "bytes": len(output.encode("utf-8")),
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
