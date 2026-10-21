"""Restructure App.vue's template into the Split Stage shell.

The route content is untouched: only the outer shell is rebuilt, every ax- class
is renamed to bg-, and the page-level components move into the narrative column.
"""

from __future__ import annotations

import re
from pathlib import Path

APP = Path(r"E:\workspace\chuangye\solana\703\website\src\App.vue")
text = APP.read_text(encoding="utf-8")

template_at = text.index("<template>")
head, template = text[:template_at], text[template_at:]

start = template.index('  <div class="ax-desk">')
end = template.index('        <Transition name="page" mode="out-in">')
shell = template[start:end]

# --- keep the pieces that must survive the shell rewrite -------------------
m = re.search(r"    <template v-if=\"menuOpen\">.*?\n    </template>\n", shell, re.S)
assert m, "drawer block not found"
drawer = m.group(0)

m = re.search(r"        <div class=\"ax-alerts\">.*?\n        </div>\n", shell, re.S)
assert m, "alerts block not found"
alerts = m.group(0)

new_shell = '''  <div class="bg-frame">
    <a class="bg-skip" href="#main" @click.prevent="focusMain">Skip to content</a>

    <aside class="bg-side">
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

DRAWER
    <main id="main" class="bg-current" tabindex="-1">
ALERTS
      <Transition name="page" mode="out-in">
'''.replace("DRAWER", drawer).replace("ALERTS", alerts)

template = template[:start] + new_shell + template[end + len('        <Transition name="page" mode="out-in">\n'):]

# --- tail: drop the inner wrapper and the duplicated StatusStrip call ------
tail_old = '''        </Transition>
      </div>
    </main>

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
'''
assert tail_old in template, "tail block not found"
template = template.replace(tail_old, '''        </Transition>
    </main>
''')

# --- rename every class in the template, keep the drawer anchor id ---------
template = template.replace("ax-", "bg-")
template = template.replace('id="bg-drawer"', 'id="ax-drawer"')
template = template.replace('aria-controls="bg-drawer"', 'aria-controls="ax-drawer"')

APP.write_text(head + template, encoding="utf-8")
print("App.vue template rebuilt:", len((head + template).splitlines()), "lines")
