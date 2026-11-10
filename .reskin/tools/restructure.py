# Reskin pass 2 — rebuild the orbital shell and the per-route composition.
# Only wrappers, tags and class names change. Every text node, binding, handler,
# attribute and component prop is left byte-identical.
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
APP = os.path.join(ROOT, "src", "App.vue")

with open(APP, encoding="utf-8", newline="") as fh:
    src = fh.read()
out = src
report = []


def sub_once(pattern, repl, label, flags=re.S):
    global out
    matches = list(re.finditer(pattern, out, flags))
    if len(matches) != 1:
        print(f"FAIL {label}: expected 1 match, found {len(matches)}")
        for m in matches[:3]:
            print("   ...", repr(out[max(0, m.start() - 40): m.end() + 40]))
        sys.exit(1)
    m = matches[0]
    text = repl(m) if callable(repl) else m.expand(repl)
    out = out[: m.start()] + text + out[m.end():]
    report.append(label)


def sub_all(pattern, repl, label, expect, flags=re.S):
    global out
    matches = list(re.finditer(pattern, out, flags))
    if len(matches) != expect:
        print(f"FAIL {label}: expected {expect} matches, found {len(matches)}")
        sys.exit(1)
    out = re.sub(pattern, repl, out, flags=flags)
    report.append(f"{label} x{expect}")


# ---------------------------------------------------------------- imports
sub_once(r'import TickerNav from "\./components/TickerNav\.vue";',
         'import OrbitIndex from "./components/OrbitIndex.vue";', "import OrbitIndex")
sub_once(r'import RailNav from "\./components/RailNav\.vue";',
         'import BrandSeal from "./components/BrandSeal.vue";', "import BrandSeal")
sub_once(r'import CommandBar from "\./components/CommandBar\.vue";',
         'import StageDock from "./components/StageDock.vue";', "import StageDock")
sub_once(r'import StatusStrip from "\./components/StatusStrip\.vue";',
         'import RingColophon from "./components/RingColophon.vue";', "import RingColophon")
sub_once(r'import WalletSheet from "\./components/WalletSheet\.vue";',
         'import WalletPicker from "./components/WalletPicker.vue";', "import WalletPicker")

# ------------------------------------------------------------ thesis split
thesis_open = '        <div class="orb-thesis">\n'
start = out.index(thesis_open)
marker = '\n        </div>\n\n        <CommandBar'
end = out.index(marker)
region = out[start + len(thesis_open): end]

def reindent(text, indent):
    raw = [line.strip() for line in text.strip("\n").split("\n") if line.strip()]
    pad = " " * indent
    return "\n".join(f"{pad}{line}" for line in raw)


chunks = [c for c in re.split(r'(?=<template v-if="route === \')', region) if c.strip()]
order, cores, decks = [], [], []
for chunk in chunks:
    rid = re.search(r'<template v-if="route === \'(\w+)\'">', chunk).group(1)
    body_start = chunk.index('<div class="orb-thesis-body">') + len('<div class="orb-thesis-body">')
    body_end = chunk.rindex("</div>")
    inner = chunk[body_start: body_end].strip("\n")
    h1 = inner.index("</h1>") + len("</h1>")
    head, tail = inner[:h1], inner[h1:]
    order.append(rid)
    cores.append(
        f'              <template v-if="route === \'{rid}\'">\n'
        f'                <div class="orb-thesis-body">\n'
        f'{reindent(head, 18) if head.strip() else ""}\n'
        f'                </div>\n'
        f'              </template>\n'
    )
    decks.append(
        f'          <template v-if="route === \'{rid}\'">\n'
        f'            <div class="orb-dispatch-body">\n'
        f'{reindent(tail, 14) if tail.strip() else ""}\n'
        f'            </div>\n'
        f'          </template>\n'
    )

new_region = (
    "".join(cores)
    + '            </div>\n'          # .orb-thesis
    '          </div>\n'               # .orb-core
    '        </div>\n'                 # .orb-system
    '\n'
    '        <div class="orb-dispatch">\n'
    + "".join(decks)
    + '        </div>\n'
)
out = out[: start + len(thesis_open)] + "\n" + new_region + out[end + 1:]
report.append(f"thesis split ({', '.join(order)})")

# ------------------------------------------------------------- shell open
sub_once(
    r'<div class="orb-frame">\s*<aside class="orb-hero">\s*<RailNav />\s*'
    r'<TickerNav :tabs="navTabs" :active="route" @navigate="navigate" />\s*'
    r'<div class="orb-thesis">',
    '''<div class="orb-frame">
      <header class="orb-hero">
        <div class="orb-rings" aria-hidden="true">
          <span class="orb-ring orb-ring--outer"></span>
          <span class="orb-ring orb-ring--mid"></span>
          <span class="orb-ring orb-ring--inner"></span>
          <span class="orb-ring orb-ring--gate"></span>
          <span class="orb-sweep"></span>
        </div>

        <BrandSeal />

        <div class="orb-system">
          <OrbitIndex :tabs="navTabs" :active="route" @navigate="navigate" />

          <div class="orb-core">
            <div class="orb-thesis">''',
    "shell open",
)

# ------------------------------------------------------------ shell close
sub_once(
    r'</div>\s*<CommandBar\b(?P<props>.*?)/>\s*<StatusStrip\b.*?/>\s*</aside>',
    lambda m: "\n\n        <StageDock" + m.group("props") + "/>\n      </header>",
    "shell close",
)

# ------------------------------------------------------- footer placement
sub_once(
    r'</Transition>\s*</main>\s*</div>',
    '''</Transition>
      </main>

      <RingColophon
        :tabs="navTabs"
        :network-name="SOLANA_NETWORK_NAME"
        :cluster="SOLANA_CLUSTER"
        :program-state="programState"
        :mint-state="mintState"
        :wallet-label="walletLabel"
        :last-read="lastRead || 'Not yet'"
        @navigate="navigate"
      />
    </div>''',
    "colophon after main",
)

# --------------------------------------------------------------- wallet ui
sub_once(r'<WalletSheet\b', '<WalletPicker', "wallet picker usage")

# --------------------------------------------------- per-route composition
sub_all(
    r'<template v-if="route === \'(\w+)\'">\s*<div class="orb-canvas">',
    lambda m: f'<template v-if="route === \'{m.group(1)}\'">\n              <div class="orb-canvas orb-canvas--{m.group(1)}">',
    "canvas modifiers", 6,
)
sub_all(
    r'\s*<div class="orb-stream">(\s*)<',
    lambda m: "\n" + m.group(1) + "<",
    "stream removed", 6,
)
sub_all(
    r'\s*</div>\s*(<section class="orb-margin" aria-label="Marginal notes">)',
    lambda m: "\n                              </section>\n\n                              " + m.group(1),
    "margin promoted", 6,
)
sub_all(
    r'(</section>\s*)</section>(\s*</div>\s*</template>)',
    r'\1\2',
    "band closed", 6,
)

# home: the two sheets become a colonnade
sub_once(
    r'(\s*)<article class="orb-sheet">(\s*<div class="orb-sheet-body">\s*<header class="orb-sheet-head">\s*<h2 class="orb-sheet-title">Newest quests</h2>)',
    lambda m: f'{m.group(1)}<div class="orb-colonnade">{m.group(1)}<article class="orb-sheet">{m.group(2)}',
    "colonnade open",
)
sub_once(
    r'(\s*)<section class="orb-doors" aria-label="Ways to take part">',
    lambda m: f'{m.group(1)}</div>{m.group(1)}<section class="orb-doors" aria-label="Ways to take part">',
    "colonnade close",
)

with open(APP, "w", encoding="utf-8", newline="") as fh:
    fh.write(out)

print("applied:")
for line in report:
    print(f"  - {line}")
