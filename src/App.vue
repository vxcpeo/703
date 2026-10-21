<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from "vue";
import { useCommunityApp } from "./useCommunityApp";
import {
  SOLANA_CLUSTER,
  SOLANA_NETWORK_NAME,
  TOKEN_MINT_ADDRESS,
} from "./solana.js";
import Icon from "./Icon.vue";
import RailNav from "./components/RailNav.vue";
import CommandBar from "./components/CommandBar.vue";
import StatusStrip from "./components/StatusStrip.vue";
import WalletSheet from "./components/WalletSheet.vue";

const communityApp = useCommunityApp();
const {
  configured,
  mintConfigured,
  programReady,
  wallet,
  token,
  tokenName,
  tokenSymbol,
  tokenDecimals,
  native,
  treasury,
  treasuryKnown,
  treasuryNativeKnown,
  treasuryTokenKnown,
  treasuryError,
  totalSupply,
  treasuryBalance,
  treasuryNative,
  paused,
  quests,
  proposals,
  accountError,
  accountReading,
  accountReady,
  readError,
  reading,
  ready,
  lastRead,
  connected,
  isOwner,
  busy,
  txState,
  connecting,
  short,
  units,
  solUnits,
  date,
  explorer,
  notify,
  refresh,
  connect,
  disconnectWallet,
  walletOptions,
  walletPickerOpen,
  closeWalletPicker,
  chooseWallet,
  claimQuest: recordQuest,
  createQuest: publishQuest,
  setQuestActive: changeQuestActive,
  createProposal: publishProposal,
  castVote,
  questStatus,
  proposalStatus,
  votePercent,
} = communityApp;

/* ------------------------------------------------------------------ routes */

const routes = [
  { id: "home", label: "Overview", icon: "portico" },
  { id: "quests", label: "Quests", icon: "flag" },
  { id: "governance", label: "Votes", icon: "ballot" },
  { id: "treasury", label: "Treasury", icon: "safe" },
  { id: "stake", label: "Token", icon: "coin" },
  { id: "learn", label: "Guide", icon: "book" },
];
const validTabs = routes.map((entry) => entry.id);
const route = ref(
  validTabs.includes(location.hash.slice(1)) ? location.hash.slice(1) : "home",
);

const menuOpen = ref(false);

function syncFromHash() {
  const next = location.hash.slice(1);
  route.value = validTabs.includes(next) ? next : "home";
  menuOpen.value = false;
}

async function go(next) {
  menuOpen.value = false;
  if (route.value !== next) history.pushState(null, "", `#${next}`);
  route.value = next;
  focusMain();
  await nextTick();
  window.scrollTo({
    top: 0,
    behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
      ? "instant"
      : "smooth",
  });
}

function navigate(next) {
  go(next);
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function dismissToast() {
  txState.value = { stage: "idle", label: "", message: "", hash: "" };
}

function focusMain() {
  document.getElementById("main")?.focus({ preventScroll: true });
}

function onKeydown(event) {
  if (event.key !== "Escape") return;
  if (walletPickerOpen.value) closeWalletPicker();
  if (menuOpen.value) menuOpen.value = false;
}

onMounted(() => {
  window.addEventListener("hashchange", syncFromHash);
  window.addEventListener("popstate", syncFromHash);
  window.addEventListener("keydown", onKeydown);
});
onUnmounted(() => {
  window.removeEventListener("hashchange", syncFromHash);
  window.removeEventListener("popstate", syncFromHash);
  window.removeEventListener("keydown", onKeydown);
});

/* ---------------------------------------------------------------- overview */

const samples = [
  {
    id: "sample-1",
    sample: true,
    title: "Read the community charter",
    reward: 12n * 10n ** 9n,
    detail: "A sample welcome quest. See how a recorded row looks.",
  },
  {
    id: "sample-2",
    sample: true,
    title: "Map one useful signal",
    reward: 28n * 10n ** 9n,
    detail: "A sample research quest. Share a source-backed observation.",
  },
  {
    id: "sample-3",
    sample: true,
    title: "Review a treasury route",
    reward: 45n * 10n ** 9n,
    detail: "A sample review quest. Compare options and explain your reasoning.",
  },
];
const sampleProposals = [
  {
    id: "sample-1",
    sample: true,
    description: "Reserve a season budget for community research bounties",
    forVotes: 0n,
    againstVotes: 0n,
    endsAt: 0,
  },
];

const allQuests = computed(() => (programReady.value ? quests.value : samples));
const visibleProposals = computed(() =>
  programReady.value ? proposals.value : sampleProposals,
);
const openQuests = computed(
  () => quests.value.filter((q) => questStatus(q) === "Open").length,
);
const openProposals = computed(
  () => proposals.value.filter((p) => proposalStatus(p) === "Open").length,
);
const metricsAvailable = computed(() => programReady.value && ready.value);
const registerQuests = computed(() => allQuests.value.slice(0, 4));
const registerProposals = computed(() => visibleProposals.value.slice(0, 3));

const leadProposal = computed(() => registerProposals.value[0] || null);
const leadBreakdown = computed(() => voteBreakdown(leadProposal.value));
const leadSupport = computed(() => {
  if (!leadProposal.value || leadBreakdown.value.empty) return null;
  return votePercent(leadProposal.value);
});

const todayLabel = computed(() =>
  new Date().toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  }),
);

const programState = computed(() =>
  programReady.value
    ? "live"
    : configured.value
      ? "pending"
      : "not set",
);

const mintState = computed(() =>
  mintConfigured.value ? short(TOKEN_MINT_ADDRESS) : "none",
);

const navTabs = computed(() =>
  routes.map((entry) => {
    let badge = null;
    if (entry.id === "quests" && metricsAvailable.value) badge = openQuests.value;
    if (entry.id === "governance" && metricsAvailable.value)
      badge = openProposals.value;
    return { ...entry, badge };
  }),
);

const walletLabel = computed(() =>
  connected.value ? short(wallet.value) : "Connect wallet",
);

const previewNote = computed(() => {
  if (configured.value)
    return "The community program is not initialised on this cluster. Sample quests and proposals stay on screen, and actions submit nothing.";
  if (mintConfigured.value)
    return "Mint data is read-only and sample program rows remain until a program is configured. Actions submit nothing.";
  return "No token mint is configured and the community program is not connected. Sample rows are shown; actions submit nothing.";
});

const actionDisabled = computed(
  () =>
    busy.value ||
    connecting.value ||
    (configured.value &&
      (!ready.value ||
        reading.value ||
        paused.value ||
        (connected.value && (!accountReady.value || accountReading.value)))),
);

const tokenIdentity = computed(() => {
  if (!mintConfigured.value) return "No token mint configured";
  if (tokenName.value) return `${tokenName.value} (${tokenSymbol.value})`;
  return reading.value
    ? "Loading mint data…"
    : `SPL token (${tokenSymbol.value}); metadata pending`;
});

function pillTone(status) {
  const key = String(status || "").toLowerCase();
  if (key === "open") return "is-open";
  if (key === "sample") return "is-sample";
  if (key === "paused" || key === "expired" || key === "filled") return "is-warn";
  if (key === "claimed" || key === "voted") return "is-info";
  return "is-neutral";
}

function questProgress(q) {
  if (!q || q.sample) return 0;
  const cap = Number(q.maxClaims) || 0;
  if (!cap) return 0;
  return Math.max(0, Math.min(100, Math.round((Number(q.claims) / cap) * 100)));
}

function voteBreakdown(proposal) {
  const forVotes = Number(proposal?.forVotes ?? 0);
  const againstVotes = Number(proposal?.againstVotes ?? 0);
  const total = forVotes + againstVotes;
  if (!total) return { forPct: 0, againstPct: 0, empty: true };
  const forPct = Math.round((forVotes / total) * 100);
  return { forPct, againstPct: 100 - forPct, empty: false };
}

/* --------------------------------------------------------------- quest view */

const search = ref("");
const questFilter = ref("all");
const questFilters = computed(() =>
  programReady.value ? ["all", "open", "claimed"] : ["all", "sample"],
);
const visibleQuests = computed(() =>
  allQuests.value.filter(
    (q) =>
      (questFilter.value === "all" ||
        questStatus(q).toLowerCase() === questFilter.value) &&
      q.title.toLowerCase().includes(search.value.trim().toLowerCase()),
  ),
);

function resetFilters() {
  search.value = "";
  questFilter.value = "all";
}

async function openQuest(q) {
  resetFilters();
  await go("quests");
  const row = document.getElementById(`quest-row-${q.id}`);
  row?.focus({ preventScroll: true });
  row?.scrollIntoView({
    block: "center",
    behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
      ? "instant"
      : "smooth",
  });
}

function preview() {
  notify(
    "This is an example row. Explore the workflow here; transactions require a configured Solana program.",
    "info",
  );
}

async function claim(q) {
  if (q.sample) return preview();
  if (questStatus(q) !== "Open")
    return notify("This quest is not available to record.");
  await recordQuest(q);
}

async function setQuest(q) {
  await changeQuestActive(q, !q.active);
}

/* ------------------------------------------------------------- quest admin */

const adminTitle = ref("");
const adminDetails = ref("");
const adminMax = ref(100);
const adminDays = ref(30);

async function createQuest() {
  const title = adminTitle.value.trim();
  const details = adminDetails.value.trim();
  if (!title || new TextEncoder().encode(title).length > 80)
    return notify("Use a quest title between 1 and 80 UTF-8 bytes.");
  if (new TextEncoder().encode(details).length > 240)
    return notify("Quest details must be 240 UTF-8 bytes or fewer.");
  if (
    !Number.isInteger(Number(adminMax.value)) ||
    adminMax.value < 1 ||
    adminMax.value > 1000000
  )
    return notify("Maximum rows must be 1 to 1,000,000.");
  if (
    !Number.isInteger(Number(adminDays.value)) ||
    adminDays.value < 1 ||
    adminDays.value > 365
  )
    return notify("Expiry must be 1 to 365 whole days from today.");
  const expiry = Math.floor(Date.now() / 1000) + Number(adminDays.value) * 86400;
  if (
    await publishQuest({
      title,
      details,
      maxClaims: Number(adminMax.value),
      expiresAt: expiry,
    })
  ) {
    adminTitle.value = "";
    adminDetails.value = "";
  }
}

/* ---------------------------------------------------------------- vote view */

const proposalText = ref("");
const proposalDays = ref(7);
const composeOpen = ref(false);
const draftSaved = ref(false);
const clearedDraft = ref(null);
watch(proposalText, (text) => {
  if (text) clearedDraft.value = null;
});

const draftKey = "clepsyra-proposal-draft";
const legacyDraftKeys = [
  "tabulora-proposal-draft",
  "konvoxa-proposal-draft",
  "solstir-proposal-draft",
  "solvyrra-proposal-draft",
  "oncivra-proposal-draft",
  "pactelora-proposal-draft",
  "solkintra-proposal-draft",
  "quorivana-proposal-draft",
  "ralliva-proposal-draft",
];
try {
  const savedDraft = sessionStorage.getItem(draftKey);
  const legacyDraft = savedDraft
    ? null
    : legacyDraftKeys.map((key) => sessionStorage.getItem(key)).find(Boolean);
  const draft = JSON.parse(savedDraft || legacyDraft || "null");
  if (draft && typeof draft.text === "string") {
    proposalText.value = draft.text.slice(0, 2000);
    proposalDays.value =
      Number.isInteger(draft.days) && draft.days >= 1 && draft.days <= 30
        ? draft.days
        : 7;
    draftSaved.value = Boolean(proposalText.value.trim());
    if (legacyDraft)
      sessionStorage.setItem(
        draftKey,
        JSON.stringify({ text: proposalText.value, days: proposalDays.value }),
      );
    legacyDraftKeys.forEach((key) => sessionStorage.removeItem(key));
  }
} catch {
  /* Draft persistence is optional when browser storage is unavailable. */
}

watch([proposalText, proposalDays], ([text, days]) => {
  try {
    if (text.trim())
      sessionStorage.setItem(
        draftKey,
        JSON.stringify({ text, days: Number(days) }),
      );
    else sessionStorage.removeItem(draftKey);
    draftSaved.value = Boolean(text.trim());
  } catch {
    draftSaved.value = false;
  }
});

async function toggleCompose() {
  composeOpen.value = !composeOpen.value;
  await nextTick();
  document
    .getElementById(composeOpen.value ? "proposal-description" : "compose-toggle")
    ?.focus();
}

function clearDraft() {
  clearedDraft.value = { text: proposalText.value, days: proposalDays.value };
  proposalText.value = "";
  proposalDays.value = 7;
  document.getElementById("proposal-description")?.focus();
}

function undoClearDraft() {
  if (!clearedDraft.value || proposalText.value) return;
  const draft = clearedDraft.value;
  clearedDraft.value = null;
  proposalText.value = draft.text;
  proposalDays.value = draft.days;
  document.getElementById("proposal-description")?.focus();
}

async function createProposal() {
  const description = proposalText.value.trim();
  if (description.length < 10 || description.length > 2000)
    return notify("Use 10 to 2,000 characters for a proposal.");
  if (
    !Number.isInteger(Number(proposalDays.value)) ||
    proposalDays.value < 1 ||
    proposalDays.value > 30
  )
    return notify("Voting duration must be 1 to 30 whole days.");
  const submittedDays = Number(proposalDays.value);
  if (await publishProposal(description, submittedDays)) {
    if (
      proposalText.value.trim() === description &&
      Number(proposalDays.value) === submittedDays
    ) {
      proposalText.value = "";
      composeOpen.value = false;
      await nextTick();
      document.getElementById("compose-toggle")?.focus();
    }
  }
}

async function vote(p, support) {
  if (p.sample) return preview();
  if (proposalStatus(p) !== "Open")
    return notify("Voting is closed or this wallet already voted.");
  await castVote(p, support);
}
</script>

<template>
  <div class="bg-frame">
    <a class="bg-skip" href="#main" @click.prevent="focusMain">Skip to content</a>

    <aside class="bg-narrative">
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

    <template v-if="menuOpen">
      <div class="bg-veil" @click="menuOpen = false"></div>
      <div id="ax-drawer" class="bg-drawer" aria-label="Sections and wallet" role="complementary">
        <header class="bg-drawer-head">
          <span class="bg-drawer-title">Clepsyra</span>
          <button class="bg-command-icon" type="button" aria-label="Close menu" @click="menuOpen = false">
            <Icon name="close" :size="18" />
          </button>
        </header>
        <nav class="bg-drawer-nav" aria-label="Sections">
          <button
            v-for="tab in navTabs"
            :key="tab.id"
            class="bg-drawer-link"
            type="button"
            :aria-current="route === tab.id ? 'page' : undefined"
            @click="navigate(tab.id)"
          >
            <Icon :name="tab.icon" :size="18" />
            <span>{{ tab.label }}</span>
            <b v-if="tab.badge !== null && tab.badge !== undefined">{{ tab.badge }}</b>
          </button>
        </nav>
        <div class="bg-drawer-foot">
          <button
            class="bg-btn bg-btn--fill bg-btn--wide"
            type="button"
            :disabled="connecting || busy"
            @click="connected ? disconnectWallet() : connect()"
          >
            <Icon name="wallet" :size="16" />
            {{ connected ? "Disconnect wallet" : "Connect wallet" }}
          </button>
          <div class="bg-drawer-facts">
            <span>Cluster <b>{{ SOLANA_CLUSTER }}</b></span>
            <span>Program <b>{{ programState }}</b></span>
            <span>Wallet <b>{{ walletLabel }}</b></span>
          </div>
        </div>
      </div>
    </template>

    <main id="main" class="bg-current" tabindex="-1">
        <div class="bg-alerts">
          <div v-if="!programReady" class="bg-alert">
            <span class="bg-alert-glyph"><Icon name="info" :size="18" /></span>
            <div class="bg-alert-copy">
              <strong>Preview rows</strong>
              <p>{{ previewNote }}</p>
            </div>
            <button class="bg-btn bg-btn--ghost bg-btn--sm bg-alert-action" type="button" @click="go('learn')">
              How it works <Icon name="arrow-right" :size="14" />
            </button>
          </div>

          <div v-if="paused" class="bg-alert" role="status">
            <span class="bg-alert-glyph"><Icon name="alert" :size="18" /></span>
            <div class="bg-alert-copy">
              <strong>Writes are paused</strong>
              <p>The program is paused. Reads continue; transactions are unavailable.</p>
            </div>
          </div>

          <div v-if="readError" class="bg-alert" data-tone="danger" role="alert">
            <span class="bg-alert-glyph"><Icon name="alert" :size="18" /></span>
            <div class="bg-alert-copy">
              <strong>Sync failed</strong>
              <p>{{ readError }}</p>
            </div>
            <button class="bg-btn bg-btn--ghost bg-btn--sm bg-alert-action" type="button" :disabled="reading || busy" @click="refresh">
              Try again
            </button>
          </div>

          <div v-if="accountError" class="bg-alert" data-tone="danger" role="alert">
            <span class="bg-alert-glyph"><Icon name="alert" :size="18" /></span>
            <div class="bg-alert-copy">
              <strong>Wallet read failed</strong>
              <p>{{ accountError }}</p>
            </div>
          </div>

          <div v-if="accountReading" class="bg-alert" data-tone="info" role="status">
            <span class="bg-alert-glyph"><Icon name="clock" :size="18" /></span>
            <div class="bg-alert-copy">
              <strong>Reading wallet balances…</strong>
            </div>
          </div>
        </div>

      <Transition name="page" mode="out-in">
          <section :key="route" class="bg-view">
            <!-- ============================================ OVERVIEW ==== -->
            <template v-if="route === 'home'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>
                  {{ SOLANA_NETWORK_NAME }} · open record
                </p>
                <h1 id="hero-title" class="bg-display">
                  Time on the<br /><em>record.</em>
                </h1>
                <p class="bg-lede">
                  Clepsyra writes down who took part, how the room voted and where
                  the money sits — a public register, stamped hour by hour, that
                  anyone can reopen. No private minutes, no unlisted spreadsheet.
                </p>
                <div class="bg-actions">
                  <button class="bg-btn bg-btn--fill bg-btn--lg" type="button" @click="go('quests')">
                    Browse quests <Icon name="arrow-right" :size="16" />
                  </button>
                  <button class="bg-btn bg-btn--line bg-btn--lg" type="button" @click="go('governance')">
                    <Icon name="ballot" :size="16" /> Open votes
                  </button>
                </div>
                <ul class="bg-facts">
                  <li><Icon name="shield" :size="15" /><span>No token mint exists</span></li>
                  <li><Icon name="users" :size="15" /><span>One row per wallet</span></li>
                  <li><Icon name="clock" :size="15" /><span>Reads refresh on demand</span></li>
                </ul>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <section class="bg-readout" aria-label="Live readouts">
                    <div class="bg-readout-head">
                      <h2 class="bg-readout-title">On the record today</h2>
                      <span class="bg-readout-date">{{ todayLabel }}</span>
                    </div>
                    <div class="bg-readout-grid">
                      <div class="bg-readout-cell">
                        <span class="bg-readout-label">Open quests</span>
                        <strong class="bg-readout-value">{{ metricsAvailable ? openQuests : "—" }}</strong>
                        <span class="bg-readout-note">
                          {{ metricsAvailable ? "read from the program" : "sample rows shown" }}
                        </span>
                      </div>
                      <div class="bg-readout-cell">
                        <span class="bg-readout-label">Votes open</span>
                        <strong class="bg-readout-value">{{ metricsAvailable ? openProposals : "—" }}</strong>
                        <span class="bg-readout-note">advisory · one vote per wallet</span>
                      </div>
                      <div class="bg-readout-cell">
                        <span class="bg-readout-label">Your wallet</span>
                        <strong class="bg-readout-value bg-readout-value--text">
                          {{ connected ? short(wallet) : "—" }}
                        </strong>
                        <span class="bg-readout-note">
                          {{
                            connected && accountReady
                              ? solUnits(native, 4) + " SOL"
                              : connected
                                ? "reading…"
                                : "not connected"
                          }}
                        </span>
                      </div>
                      <div class="bg-readout-cell">
                        <span class="bg-readout-label">Token</span>
                        <strong class="bg-readout-value bg-readout-value--text">
                          {{ mintConfigured ? tokenSymbol || "mint set" : "None yet" }}
                        </strong>
                        <span class="bg-readout-note">
                          {{ mintConfigured ? short(TOKEN_MINT_ADDRESS) : "nothing to buy or hold" }}
                        </span>
                      </div>
                    </div>
                    <div class="bg-readout-foot">
                      <span class="bg-live-dot" :class="{ 'bg-live-dot--idle': !programReady }" aria-hidden="true"></span>
                      <span>{{ programReady ? "Program reports live" : "Preview mode · nothing is submitted" }}</span>
                      <button class="bg-link" type="button" @click="go('learn')">
                        Why? <Icon name="arrow-right" :size="14" />
                      </button>
                    </div>
                  </section>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Newest quests</h2>
                      <button class="bg-link" type="button" @click="go('quests')">
                        All quests <Icon name="arrow-right" :size="14" />
                      </button>
                    </div>
                    <ul v-if="registerQuests.length" class="bg-ledger">
                      <li v-for="(q, index) in registerQuests" :key="q.id">
                        <button class="bg-ledger-row" type="button" @click="openQuest(q)">
                          <span class="bg-ledger-index">{{ String(index + 1).padStart(2, "0") }}</span>
                          <span class="bg-ledger-main">
                            <b class="bg-ledger-title">{{ q.title }}</b>
                            <small class="bg-ledger-note">
                              {{
                                q.sample
                                  ? "Sample row · preview only"
                                  : "Quest / " + String(q.id).padStart(3, "0")
                              }}
                            </small>
                          </span>
                          <span class="bg-pill" :data-tone="pillTone(questStatus(q))">{{ questStatus(q) }}</span>
                          <span class="bg-ledger-go" aria-hidden="true"><Icon name="arrow-right" :size="16" /></span>
                        </button>
                      </li>
                    </ul>
                    <div v-else class="bg-board-body">
                      <div class="bg-empty">
                        <span class="bg-empty-glyph"><Icon name="flag" :size="20" /></span>
                        <h3 class="bg-empty-title">No rows yet</h3>
                        <p class="bg-empty-text">Quests appear here once the community publishes them.</p>
                      </div>
                    </div>
                  </section>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Votes on the floor</h2>
                      <button class="bg-link" type="button" @click="go('governance')">
                        All votes <Icon name="arrow-right" :size="14" />
                      </button>
                    </div>
                    <ul v-if="registerProposals.length" class="bg-ledger">
                      <li v-for="(p, index) in registerProposals" :key="p.id">
                        <button class="bg-ledger-row" type="button" @click="go('governance')">
                          <span class="bg-ledger-index">{{ String(index + 1).padStart(2, "0") }}</span>
                          <span class="bg-ledger-main">
                            <b class="bg-ledger-title">{{ p.description }}</b>
                            <small class="bg-ledger-note">
                              {{ p.sample ? "Sample proposal · no live votes" : "Closes " + date(p.endsAt) }}
                            </small>
                          </span>
                          <span class="bg-pill" :data-tone="pillTone(proposalStatus(p))">{{ proposalStatus(p) }}</span>
                          <span class="bg-ledger-go" aria-hidden="true"><Icon name="arrow-right" :size="16" /></span>
                        </button>
                      </li>
                    </ul>
                    <div v-else class="bg-board-body">
                      <div class="bg-empty">
                        <span class="bg-empty-glyph"><Icon name="ballot" :size="20" /></span>
                        <h3 class="bg-empty-title">The floor is open</h3>
                        <p class="bg-empty-text">Start the first proposal when the community has a decision to make.</p>
                      </div>
                    </div>
                    <div v-if="registerProposals.length" class="bg-board-body">
                      <span class="bg-sheet-note">Support on the leading proposal</span>
                      <div class="bg-tally">
                        <i class="bg-tally-for" :style="{ width: leadBreakdown.forPct + '%' }"></i>
                        <i class="bg-tally-against" :style="{ width: leadBreakdown.againstPct + '%' }"></i>
                      </div>
                      <div class="bg-tally-keys">
                        <span class="bg-tally-key">
                          For <b>{{ units(leadProposal?.forVotes || 0n) }}</b>
                        </span>
                        <span class="bg-tally-key bg-tally-key--against">
                          Against <b>{{ units(leadProposal?.againstVotes || 0n) }}</b>
                        </span>
                        <span>
                          Support <b>{{ leadSupport === null ? "—" : leadSupport + "%" }}</b>
                        </span>
                      </div>
                    </div>
                  </section>

                  <section class="bg-forks" aria-label="Ways to take part">
                    <article class="bg-fork">
                      <span class="bg-fork-glyph"><Icon name="flag" :size="22" /></span>
                      <h2>Take part</h2>
                      <p>
                        Pick a quest, record your participation and leave a row anyone can
                        check later. Rows are participation only — they do not pay a token.
                      </p>
                      <div class="bg-fork-foot">
                        <button class="bg-btn bg-btn--line" type="button" @click="go('quests')">
                          See {{ allQuests.length }} quests <Icon name="arrow-right" :size="15" />
                        </button>
                      </div>
                    </article>
                    <article class="bg-fork bg-fork--ballot">
                      <span class="bg-fork-glyph"><Icon name="ballot" :size="22" /></span>
                      <h2>Weigh in</h2>
                      <p>
                        Write a proposal, set a window between one and thirty days, and let
                        wallets answer. Results are advisory and never move funds.
                      </p>
                      <div class="bg-fork-foot">
                        <button class="bg-btn bg-btn--fill" type="button" @click="go('governance')">
                          Open the floor <Icon name="arrow-right" :size="15" />
                        </button>
                      </div>
                    </article>
                  </section>
                </div>

                <div class="bg-margin">
                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Your wallet</h2>
                      <span class="bg-sheet-note">{{ connected ? "connected" : "idle" }}</span>
                    </div>
                    <div class="bg-sheet-body bg-sheet-body--flush">
                      <dl class="bg-factlist">
                        <div class="bg-fact">
                          <dt>Address</dt>
                          <dd>{{ connected ? short(wallet) : "not connected" }}</dd>
                        </div>
                        <div class="bg-fact">
                          <dt>SOL</dt>
                          <dd>{{ connected && accountReady ? solUnits(native, 4) : "—" }}</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>{{ mintConfigured ? tokenSymbol : "Token" }}</dt>
                          <dd>
                            {{ mintConfigured && connected && accountReady ? units(token) : "not configured" }}
                          </dd>
                        </div>
                        <div class="bg-fact">
                          <dt>State</dt>
                          <dd>
                            {{ connected ? (accountReady ? "synced" : "reading") : "connect to read" }}
                          </dd>
                        </div>
                      </dl>
                    </div>
                    <div class="bg-sheet-foot">
                      <button
                        class="bg-btn bg-btn--fill bg-btn--wide"
                        type="button"
                        :disabled="connecting || busy"
                        @click="connected ? disconnectWallet() : connect()"
                      >
                        <Icon name="wallet" :size="15" />
                        {{ connected ? "Disconnect wallet" : "Connect wallet" }}
                      </button>
                    </div>
                  </section>

                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Token</h2>
                      <span class="bg-pill" data-tone="is-neutral">{{ mintConfigured ? "configured" : "none yet" }}</span>
                    </div>
                    <div class="bg-sheet-body">
                      <p>{{ tokenIdentity }}</p>
                      <p>
                        The community program records participation and advisory votes.
                        It never mints, holds or pays out a token.
                      </p>
                      <button class="bg-btn bg-btn--line bg-btn--wide" type="button" @click="go('stake')">
                        Token status <Icon name="arrow-right" :size="14" />
                      </button>
                    </div>
                  </section>

                  <div class="bg-note">
                    <Icon name="shield" :size="18" />
                    <div>
                      <strong>Before you sign</strong>
                      <p>Your wallet reviews every instruction. A preview row never sends a transaction.</p>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- ============================================== QUESTS ==== -->
            <template v-if="route === 'quests'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>Participation
                </p>
                <h1 class="bg-display">Find your <em>part in it.</em></h1>
                <p class="bg-lede">
                  Each quest is an open invitation to take part. Recording one writes a
                  single row for your wallet — it does not verify off-chain work, prove
                  a unique person or pay a token.
                </p>
                <div class="bg-tags">
                  <span class="bg-tag bg-tag--strong">{{ allQuests.length }} rows</span>
                  <span class="bg-tag">{{ programReady ? "program live" : "preview" }}</span>
                </div>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <div class="bg-console-line">
                    <label class="bg-search">
                      <Icon name="search" :size="17" />
                      <span class="visually-hidden">Search quests</span>
                      <input class="bg-search-input" v-model="search" type="search" placeholder="Search quests…" autocomplete="off" />
                    </label>
                    <div class="bg-chips" role="group" aria-label="Filter quests">
                      <button
                        v-for="f in questFilters"
                        :key="f"
                        class="bg-chip"
                        :aria-pressed="questFilter === f"
                        type="button"
                        @click="questFilter = f"
                      >
                        {{ f }}
                      </button>
                    </div>
                    <span class="bg-count" role="status">
                      {{ visibleQuests.length }} {{ visibleQuests.length === 1 ? "quest" : "quests" }}
                    </span>
                  </div>

                  <div
                    v-if="reading && !allQuests.length"
                    class="bg-board bg-board--loading"
                    role="status"
                    aria-label="Loading quests"
                  >
                    <div v-for="i in 3" :key="i" class="bg-loading"></div>
                  </div>

                  <div v-else-if="!visibleQuests.length" class="bg-empty">
                    <span class="bg-empty-glyph"><Icon name="flag" :size="20" /></span>
                    <h3 class="bg-empty-title">
                      {{
                        readError
                          ? "Rows unavailable"
                          : search || questFilter !== "all"
                            ? "No matching quests"
                            : "Room for the first row"
                      }}
                    </h3>
                    <p class="bg-empty-text">
                      {{
                        readError
                          ? "Refresh the connection to read the latest quests."
                          : search || questFilter !== "all"
                            ? "Try another keyword or show every quest."
                            : "No quests have been published yet. Check back for the next activity."
                      }}
                    </p>
                    <button
                      v-if="search || questFilter !== 'all'"
                      class="bg-btn bg-btn--line"
                      type="button"
                      @click="resetFilters"
                    >
                      Clear filters
                    </button>
                    <button
                      v-else-if="readError"
                      class="bg-btn bg-btn--fill"
                      type="button"
                      :disabled="reading"
                      @click="refresh"
                    >
                      Try again
                    </button>
                  </div>

                  <div v-else class="bg-board">
                    <article
                      v-for="(q, index) in visibleQuests"
                      :id="'quest-row-' + q.id"
                      :key="q.id"
                      class="bg-entry"
                      tabindex="-1"
                    >
                      <div class="bg-entry-head">
                        <span class="bg-pill" :data-tone="pillTone(questStatus(q))">{{ questStatus(q) }}</span>
                        <span class="bg-entry-id">
                          {{ q.sample ? "sample" : "quest " + String(index + 1).padStart(2, "0") }}
                        </span>
                      </div>
                      <h3 class="bg-entry-title">{{ q.title }}</h3>
                      <p class="bg-entry-text">{{ q.detail || "Community participation record." }}</p>
                      <div class="bg-entry-meter">
                        <div class="bg-entry-meter-row">
                          <span>Capacity</span>
                          <b>{{ q.sample ? "preview only" : q.claims + " / " + q.maxClaims }}</b>
                        </div>
                        <div class="bg-gauge"><i class="bg-gauge-fill" :style="{ width: questProgress(q) + '%' }"></i></div>
                        <div class="bg-entry-meter-row">
                          <span>Expires</span>
                          <b>{{ q.sample ? "—" : date(q.expiresAt) }}</b>
                        </div>
                      </div>
                      <div class="bg-entry-foot">
                        <button
                          class="bg-btn bg-btn--fill bg-btn--sm"
                          type="button"
                          :disabled="actionDisabled || (!q.sample && questStatus(q) !== 'Open')"
                          @click="claim(q)"
                        >
                          {{
                            q.sample
                              ? "Preview row"
                              : q.claimed
                                ? "Recorded"
                                : questStatus(q) !== "Open"
                                  ? questStatus(q)
                                  : connected
                                    ? "Record my part"
                                    : "Connect to record"
                          }}
                        </button>
                        <button
                          v-if="isOwner && !q.sample"
                          class="bg-btn bg-btn--line bg-btn--sm"
                          type="button"
                          :disabled="busy"
                          @click="setQuest(q)"
                        >
                          {{ q.active ? "Pause" : "Resume" }}
                        </button>
                      </div>
                    </article>
                  </div>
                </div>

                <div class="bg-margin">
                  <form v-if="isOwner" class="bg-sheet bg-form" @submit.prevent="createQuest">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Publish a quest</h2>
                      <span class="bg-tag">authority wallet</span>
                    </div>
                    <div class="bg-sheet-body">
                      <label class="bg-field">
                        <span class="bg-field-label">Quest title</span>
                        <input class="bg-input" v-model="adminTitle" maxlength="80" required placeholder="Welcome to the community" />
                      </label>
                      <label class="bg-field">
                        <span class="bg-field-label">Details</span>
                        <input class="bg-input" v-model="adminDetails" maxlength="240" placeholder="What should participants review?" />
                      </label>
                      <label class="bg-field">
                        <span class="bg-field-label">Maximum rows</span>
                        <input class="bg-input" v-model="adminMax" type="number" min="1" max="1000000" required />
                      </label>
                      <label class="bg-field">
                        <span class="bg-field-label">Open for (days)</span>
                        <input class="bg-input" v-model="adminDays" type="number" min="1" max="365" required />
                      </label>
                      <p class="bg-form-note">Rows record participation only. No token reward is attached.</p>
                      <button class="bg-btn bg-btn--fill" type="submit" :disabled="actionDisabled">
                        <Icon name="plus" :size="15" /> Publish quest
                      </button>
                    </div>
                  </form>

                  <div class="bg-note">
                    <Icon name="shield" :size="18" />
                    <div>
                      <strong>Your wallet, your decision</strong>
                      <p>Review the quest and the network before confirming. A preview never sends a transaction.</p>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- =============================================== VOTES ==== -->
            <template v-if="route === 'governance'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>Advisory votes
                </p>
                <h1 class="bg-display">Put it <em>to the room.</em></h1>
                <p class="bg-lede">
                  Write a proposal, choose a window of one to thirty days, and let
                  wallets answer. One vote per wallet; results are advisory and never
                  move funds.
                </p>
                <div class="bg-tags">
                  <span class="bg-tag bg-tag--strong">{{ visibleProposals.length }} proposals</span>
                  <span class="bg-tag">{{ programReady ? "on chain" : "sample rows" }}</span>
                </div>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <section class="bg-board">
                    <template v-if="visibleProposals.length">
                      <article v-for="p in visibleProposals" :key="p.id" class="bg-ballot">
                        <div class="bg-ballot-head">
                          <span class="bg-ballot-id">
                            {{ p.sample ? "sample proposal" : "proposal " + String(p.id).padStart(3, "0") }}
                          </span>
                          <span class="bg-pill" :data-tone="pillTone(proposalStatus(p))">{{ proposalStatus(p) }}</span>
                        </div>
                        <h3 class="bg-ballot-title">{{ p.description }}</h3>
                        <div class="bg-tally">
                          <i class="bg-tally-for" :style="{ width: voteBreakdown(p).forPct + '%' }"></i>
                          <i class="bg-tally-against" :style="{ width: voteBreakdown(p).againstPct + '%' }"></i>
                        </div>
                        <div class="bg-tally-keys">
                          <span class="bg-tally-key">For <b>{{ units(p.forVotes) }}</b></span>
                          <span class="bg-tally-key bg-tally-key--against">Against <b>{{ units(p.againstVotes) }}</b></span>
                          <span>
                            {{ voteBreakdown(p).empty ? "No votes yet" : votePercent(p) + "% support" }}
                          </span>
                          <span v-if="!p.sample">Closes {{ date(p.endsAt) }}</span>
                        </div>
                        <div class="bg-ballot-foot">
                          <p>
                            {{
                              p.voted
                                ? "Your vote is on the record."
                                : voteBreakdown(p).empty
                                  ? "Waiting for the first vote."
                                  : "Advisory only — nothing is executed."
                            }}
                          </p>
                          <button
                            class="bg-btn bg-btn--fill bg-btn--sm"
                            type="button"
                            :disabled="actionDisabled || (!p.sample && proposalStatus(p) !== 'Open')"
                            @click="vote(p, true)"
                          >
                            <Icon name="check" :size="14" /> Vote for
                          </button>
                          <button
                            class="bg-btn bg-btn--line bg-btn--sm"
                            type="button"
                            :disabled="actionDisabled || (!p.sample && proposalStatus(p) !== 'Open')"
                            @click="vote(p, false)"
                          >
                            <Icon name="close" :size="14" /> Against
                          </button>
                        </div>
                      </article>
                    </template>

                    <div v-else-if="programReady && reading" class="bg-board-body" role="status">
                      <span class="visually-hidden">Loading proposals</span>
                    </div>

                    <div v-else class="bg-board-body">
                      <div class="bg-empty">
                        <span class="bg-empty-glyph"><Icon name="ballot" :size="20" /></span>
                        <h3 class="bg-empty-title">{{ readError ? "Proposals unavailable" : "The floor is open" }}</h3>
                        <p class="bg-empty-text">
                          {{
                            readError
                              ? "Refresh the connection to reconnect."
                              : "Start the first proposal with one clear decision and a voting window."
                          }}
                        </p>
                        <button
                          v-if="!readError && !composeOpen"
                          class="bg-btn bg-btn--fill"
                          type="button"
                          @click="toggleCompose"
                        >
                          Write the first proposal
                        </button>
                      </div>
                    </div>
                  </section>

                  <div class="bg-note">
                    <Icon name="info" :size="18" />
                    <div>
                      <strong>Advisory, not binding</strong>
                      <p>Votes do not execute treasury spending. Weight follows the program's own rules.</p>
                    </div>
                  </div>
                </div>

                <div class="bg-margin">
                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Start a proposal</h2>
                      <span class="bg-sheet-note">
                        {{ draftSaved && !composeOpen ? "draft saved" : "10–2,000 chars" }}
                      </span>
                    </div>
                    <div class="bg-sheet-body">
                      <button
                        id="compose-toggle"
                        class="bg-btn bg-btn--line bg-btn--wide"
                        type="button"
                        :aria-expanded="composeOpen"
                        aria-controls="compose-editor"
                        @click="toggleCompose"
                      >
                        <Icon :name="composeOpen ? 'close' : 'plus'" :size="15" />
                        {{
                          composeOpen
                            ? "Close editor"
                            : draftSaved
                              ? "Continue your draft"
                              : "New proposal"
                        }}
                      </button>
                    </div>
                    <form
                      v-if="composeOpen"
                      id="compose-editor"
                      class="bg-sheet-body bg-form"
                      @submit.prevent="createProposal"
                      @keydown.esc.prevent="toggleCompose"
                    >
                      <label class="bg-field">
                        <span class="bg-field-label">Proposal</span>
                        <textarea
                          id="proposal-description"
                          class="bg-textarea"
                          v-model="proposalText"
                          minlength="10"
                          maxlength="2000"
                          required
                          placeholder="One decision, its purpose, any budget, and the outcome you expect."
                        ></textarea>
                      </label>
                      <label class="bg-field">
                        <span class="bg-field-label">Voting window (days)</span>
                        <input class="bg-input" v-model="proposalDays" type="number" min="1" max="30" required />
                      </label>
                      <div class="bg-form-foot">
                        <span class="bg-form-note">{{ proposalText.length }} / 2,000</span>
                        <button
                          class="bg-btn bg-btn--fill"
                          type="submit"
                          :disabled="actionDisabled || proposalText.trim().length < 10"
                        >
                          {{ programReady ? "Publish" : "Preview" }}
                        </button>
                      </div>
                      <div class="bg-form-actions">
                        <button class="bg-btn bg-btn--ghost bg-btn--sm" type="button" @click="toggleCompose">
                          Keep draft
                        </button>
                        <button
                          v-if="proposalText"
                          class="bg-btn bg-btn--ghost bg-btn--sm"
                          type="button"
                          @click="clearDraft"
                        >
                          Clear
                        </button>
                        <button
                          v-else-if="clearedDraft"
                          class="bg-btn bg-btn--ghost bg-btn--sm"
                          type="button"
                          @click="undoClearDraft"
                        >
                          Undo clear
                        </button>
                      </div>
                    </form>
                  </section>

                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">What lands</h2>
                      <span class="bg-sheet-note">three moves</span>
                    </div>
                    <div class="bg-sheet-body bg-sheet-body--flush">
                      <ol class="bg-steps">
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">1</span>
                          <div class="bg-step-body">
                            <h3>One decision</h3>
                            <p>State a single decision and why it matters now.</p>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">2</span>
                          <div class="bg-step-body">
                            <h3>Context and cost</h3>
                            <p>Name the outcome and any budget the room should expect.</p>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">3</span>
                          <div class="bg-step-body">
                            <h3>Time to answer</h3>
                            <p>Give wallets 1–30 days so the vote is not a reflex.</p>
                          </div>
                        </li>
                      </ol>
                    </div>
                  </section>
                </div>
              </div>
            </template>

            <!-- ============================================ TREASURY ==== -->
            <template v-if="route === 'treasury'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>Public reads
                </p>
                <h1 class="bg-display">Nothing hidden <em>in the books.</em></h1>
                <p class="bg-lede">
                  Treasury balances and account rows are read straight from Solana.
                  When a read is unavailable, this page says so instead of guessing.
                </p>
                <div class="bg-tags">
                  <span class="bg-tag bg-tag--strong">{{ SOLANA_NETWORK_NAME }}</span>
                </div>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <section class="bg-meters" aria-label="Treasury reads">
                    <div class="bg-meter">
                      <span class="bg-meter-label">Treasury token</span>
                      <b class="bg-meter-value">{{ ready && treasuryTokenKnown ? units(treasuryBalance) : "—" }}</b>
                      <span class="bg-meter-note">{{ tokenIdentity }}</span>
                    </div>
                    <div class="bg-meter">
                      <span class="bg-meter-label">Treasury SOL</span>
                      <b class="bg-meter-value">
                        {{ ready && treasuryNativeKnown ? solUnits(treasuryNative, 4) : "—" }}
                      </b>
                      <span class="bg-meter-note">native balance for fees</span>
                    </div>
                    <div class="bg-meter">
                      <span class="bg-meter-label">Issued supply</span>
                      <b class="bg-meter-value">{{ mintConfigured && ready ? units(totalSupply) : "—" }}</b>
                      <span class="bg-meter-note">read from the mint</span>
                    </div>
                    <div class="bg-meter">
                      <span class="bg-meter-label">Activity index</span>
                      <b class="bg-meter-value">None</b>
                      <span class="bg-meter-note">no indexer connected yet</span>
                    </div>
                  </section>

                  <p
                    v-if="treasuryError || (mintConfigured && ready && (!treasuryKnown || !treasuryTokenKnown))"
                    class="bg-form-note"
                    role="status"
                  >
                    {{ treasuryError || "Treasury token or SOL balances are not fully available yet." }}
                  </p>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Account statement</h2>
                      <span class="bg-sheet-note">{{ ready ? "read at " + lastRead : "awaiting read" }}</span>
                    </div>
                    <div class="bg-statement">
                      <div class="bg-statement-row">
                        <span class="bg-statement-key">On-chain token</span>
                        <span class="bg-statement-leader" aria-hidden="true"></span>
                        <span class="bg-statement-val bg-statement-val--muted">{{ tokenIdentity }}</span>
                      </div>
                      <div class="bg-statement-row">
                        <span class="bg-statement-key">
                          {{ mintConfigured ? "Total issued " + tokenSymbol : "Issued supply" }}
                        </span>
                        <span class="bg-statement-leader" aria-hidden="true"></span>
                        <span class="bg-statement-val">
                          {{ mintConfigured && ready ? units(totalSupply) : "—" }}
                        </span>
                      </div>
                      <div class="bg-statement-row">
                        <span class="bg-statement-key">Token staking</span>
                        <span class="bg-statement-leader" aria-hidden="true"></span>
                        <span class="bg-statement-val bg-statement-val--muted">not implemented</span>
                      </div>
                      <div class="bg-statement-row">
                        <span class="bg-statement-key">
                          {{ mintConfigured ? "Your " + tokenSymbol : "Your token balance" }}
                        </span>
                        <span class="bg-statement-leader" aria-hidden="true"></span>
                        <span class="bg-statement-val">
                          {{
                            connected && accountReady
                              ? units(token)
                              : connected
                                ? "reading"
                                : "connect wallet"
                          }}
                        </span>
                      </div>
                      <div class="bg-statement-row">
                        <span class="bg-statement-key">Decimals</span>
                        <span class="bg-statement-leader" aria-hidden="true"></span>
                        <span class="bg-statement-val bg-statement-val--muted">{{ mintConfigured ? tokenDecimals : "—" }}</span>
                      </div>
                    </div>
                  </section>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Activity</h2>
                      <span class="bg-sheet-note">not connected</span>
                    </div>
                    <div class="bg-board-body">
                      <div class="bg-empty">
                        <span class="bg-empty-glyph"><Icon name="clock" :size="20" /></span>
                        <h3 class="bg-empty-title">
                          {{
                            reading
                              ? "Reading the chain…"
                              : readError
                                ? "Activity could not load"
                                : "No indexer yet"
                          }}
                        </h3>
                        <p class="bg-empty-text">
                          A Solana activity index will be connected after the program is
                          deployed for production use.
                        </p>
                      </div>
                    </div>
                  </section>
                </div>

                <div class="bg-margin">
                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Addresses</h2>
                    </div>
                    <div class="bg-sheet-body bg-sheet-body--flush">
                      <dl class="bg-factlist">
                        <div class="bg-fact">
                          <dt>Treasury wallet</dt>
                          <dd>
                            <a
                              v-if="treasury"
                              :href="explorer('address', treasury)"
                              target="_blank"
                              rel="noopener noreferrer"
                            >{{ short(treasury) }} <Icon name="arrow-up-right" :size="13" /></a>
                            <span v-else class="bg-fact-quiet">not available</span>
                          </dd>
                        </div>
                        <div class="bg-fact">
                          <dt>Token mint</dt>
                          <dd>
                            <a
                              v-if="mintConfigured"
                              :href="explorer('address', TOKEN_MINT_ADDRESS)"
                              target="_blank"
                              rel="noopener noreferrer"
                            >{{ short(TOKEN_MINT_ADDRESS) }} <Icon name="arrow-up-right" :size="13" /></a>
                            <span v-else class="bg-fact-quiet">not configured</span>
                          </dd>
                        </div>
                        <div class="bg-fact">
                          <dt>Cluster</dt>
                          <dd>{{ SOLANA_CLUSTER }}</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Network</dt>
                          <dd>{{ SOLANA_NETWORK_NAME }}</dd>
                        </div>
                      </dl>
                    </div>
                    <div class="bg-sheet-body">
                      <p>
                        {{
                          mintConfigured
                            ? "Decimals come from the mint; display metadata stays pending until it is verified."
                            : "No token mint is deployed or configured."
                        }}
                      </p>
                    </div>
                  </section>

                  <div class="bg-note bg-note--warn">
                    <Icon name="alert" :size="18" />
                    <div>
                      <strong>An open record cuts both ways</strong>
                      <p>Anyone can reopen these reads, including people who disagree with the last decision.</p>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- =============================================== TOKEN ==== -->
            <template v-if="route === 'stake'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>Token details
                </p>
                <h1 class="bg-display">No token is <em>wired up.</em></h1>
                <p class="bg-lede">
                  Quests and advisory votes run through the Solana program. Staking,
                  locking and rewards stay switched off until a mint and its custody
                  rules exist.
                </p>
                <div class="bg-tags">
                  <span class="bg-tag bg-tag--strong">not configured</span>
                </div>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Token status</h2>
                      <span class="bg-pill" data-tone="is-neutral">not configured</span>
                    </div>
                    <div class="bg-board-body bg-board-body--flush">
                      <dl class="bg-factlist">
                        <div class="bg-fact bg-fact--muted">
                          <dt>On-chain token</dt>
                          <dd>{{ tokenIdentity }}</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Token staking</dt>
                          <dd>not implemented</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Locking</dt>
                          <dd>not implemented</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Reward source</dt>
                          <dd>undefined</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Decimals</dt>
                          <dd>{{ mintConfigured ? tokenDecimals : "—" }}</dd>
                        </div>
                      </dl>
                    </div>
                    <div class="bg-board-body">
                      <p>
                        The program records participation rows and advisory votes. It does
                        not custody tokens, mint rewards or track staking positions.
                      </p>
                    </div>
                  </section>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">What has to exist first</h2>
                      <span class="bg-sheet-note">in order</span>
                    </div>
                    <div class="bg-board-body bg-board-body--flush">
                      <ol class="bg-steps">
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">1</span>
                          <div class="bg-step-body">
                            <h3>A verified SPL mint</h3>
                            <p>
                              The mint address, decimals and metadata would be read from
                              Solana before any label appears here.
                            </p>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">2</span>
                          <div class="bg-step-body">
                            <h3>Written custody rules</h3>
                            <p>
                              Who can move locked balances, how a holder exits, and what
                              happens if the program pauses.
                            </p>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">3</span>
                          <div class="bg-step-body">
                            <h3>A funded reward source</h3>
                            <p>
                              Rewards need money behind them. Until that exists, no reward
                              can be promised in a row.
                            </p>
                          </div>
                        </li>
                      </ol>
                    </div>
                  </section>
                </div>

                <div class="bg-margin">
                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Wiring</h2>
                    </div>
                    <div class="bg-sheet-body bg-sheet-body--flush">
                      <dl class="bg-factlist">
                        <div class="bg-fact">
                          <dt>Cluster</dt>
                          <dd>{{ SOLANA_CLUSTER }}</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Network</dt>
                          <dd>{{ SOLANA_NETWORK_NAME }}</dd>
                        </div>
                        <div class="bg-fact">
                          <dt>Program</dt>
                          <dd>{{ programState }}</dd>
                        </div>
                        <div class="bg-fact bg-fact--muted">
                          <dt>Mint</dt>
                          <dd>{{ mintState }}</dd>
                        </div>
                      </dl>
                    </div>
                    <div class="bg-sheet-foot">
                      <button class="bg-btn bg-btn--line bg-btn--wide" type="button" @click="go('learn')">
                        Read the guide <Icon name="arrow-right" :size="14" />
                      </button>
                    </div>
                  </section>

                  <div class="bg-note bg-note--warn">
                    <Icon name="alert" :size="18" />
                    <div>
                      <strong>No mint has been issued</strong>
                      <p>Anything claiming a Clepsyra token right now is not from this project.</p>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- =============================================== GUIDE ==== -->
            <template v-if="route === 'learn'">
              <div class="bg-runhead">
                <p class="bg-kicker">
                  <span class="bg-kicker-dot" aria-hidden="true"></span>The field guide
                </p>
                <h1 class="bg-display">A way in. <em>A way to check.</em></h1>
                <p class="bg-lede">
                  What each row means, what your wallet will ask you to confirm, and
                  what this project deliberately does not do yet.
                </p>
                <div class="bg-tags">
                  <span class="bg-tag bg-tag--strong">{{ SOLANA_NETWORK_NAME }}</span>
                </div>
              </div>

              <div class="bg-stage">
                <div class="bg-wide">
                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Three ways through</h2>
                      <span class="bg-sheet-note">start anywhere</span>
                    </div>
                    <div class="bg-board-body bg-board-body--flush">
                      <ol class="bg-steps">
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">1</span>
                          <div class="bg-step-body">
                            <h3>Record a participation row</h3>
                            <p>
                              Quests carry an expiry and a row cap. Each wallet records
                              once. Rows do not verify off-chain work, prove a unique
                              person, or pay a token.
                            </p>
                            <div class="bg-step-foot">
                              <button class="bg-btn bg-btn--line bg-btn--sm" type="button" @click="go('quests')">
                                See quests <Icon name="arrow-right" :size="14" />
                              </button>
                            </div>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">2</span>
                          <div class="bg-step-body">
                            <h3>Wait for real token details</h3>
                            <p>
                              Locking and rewards need a verified mint, custody rules and a
                              funded reward source. None are enabled by the community
                              program.
                            </p>
                            <div class="bg-step-foot">
                              <button class="bg-btn bg-btn--line bg-btn--sm" type="button" @click="go('stake')">
                                Token status <Icon name="arrow-right" :size="14" />
                              </button>
                            </div>
                          </div>
                        </li>
                        <li class="bg-step">
                          <span class="bg-step-num" aria-hidden="true">3</span>
                          <div class="bg-step-body">
                            <h3>Answer the next question</h3>
                            <p>
                              Create a proposal with a 1–30 day window, or vote on an open
                              one. One vote per wallet. Results are advisory.
                            </p>
                            <div class="bg-step-foot">
                              <button class="bg-btn bg-btn--line bg-btn--sm" type="button" @click="go('governance')">
                                Open votes <Icon name="arrow-right" :size="14" />
                              </button>
                            </div>
                          </div>
                        </li>
                      </ol>
                    </div>
                  </section>

                  <section class="bg-board">
                    <div class="bg-board-head">
                      <h2 class="bg-board-title">Good to know</h2>
                    </div>
                    <div class="bg-board-body bg-board-body--flush">
                      <div class="bg-faq">
                        <details class="bg-faq-item" open>
                          <summary class="bg-faq-q">What does a wallet confirmation do?</summary>
                          <p class="bg-faq-a">
                            Recording a quest row, publishing a proposal and casting a vote
                            use the initialised program on {{ SOLANA_NETWORK_NAME }}. Your
                            wallet shows every instruction before you sign.
                          </p>
                        </details>
                        <details class="bg-faq-item">
                          <summary class="bg-faq-q">Who controls the protocol?</summary>
                          <p class="bg-faq-a">
                            The program authority can publish quests and pause community
                            actions. Advisory votes do not execute treasury spending.
                          </p>
                        </details>
                        <details class="bg-faq-item">
                          <summary class="bg-faq-q">Why is the token name separate from Clepsyra?</summary>
                          <p class="bg-faq-a">
                            A future mint defines its own name, symbol and decimals.
                            Clepsyra is the application brand. Current status:
                            {{ tokenIdentity }}.
                          </p>
                        </details>
                        <details class="bg-faq-item">
                          <summary class="bg-faq-q">Is a Clepsyra token deployed?</summary>
                          <p class="bg-faq-a">
                            No Clepsyra token mint is configured. The community program
                            does not create or distribute a token.
                          </p>
                        </details>
                        <details class="bg-faq-item">
                          <summary class="bg-faq-q">Is Clepsyra an official Solana product?</summary>
                          <p class="bg-faq-a">
                            No. Clepsyra is an independent community project currently
                            reading {{ SOLANA_NETWORK_NAME }}. It is not affiliated with the
                            Solana Foundation.
                          </p>
                        </details>
                        <details class="bg-faq-item">
                          <summary class="bg-faq-q">Why do I see preview rows or a connection error?</summary>
                          <p class="bg-faq-a">
                            Preview means sample rows are shown and nothing is submitted. A
                            connection error means configured Solana data could not be read
                            — use the refresh button to retry. Never share a seed phrase or
                            private key to fix a connection.
                          </p>
                        </details>
                      </div>
                    </div>
                  </section>
                </div>

                <div class="bg-margin">
                  <section class="bg-sheet">
                    <div class="bg-sheet-head">
                      <h2 class="bg-sheet-title">Checklist</h2>
                    </div>
                    <div class="bg-sheet-body bg-sheet-body--flush">
                      <ul class="bg-checklist">
                        <li class="bg-check" :class="{ 'bg-check--done': connected }">
                          <span class="bg-check-mark">{{ connected ? "✓" : "1" }}</span>
                          <div>
                            <b>Bring a Solana wallet</b>
                            <small>{{ connected ? "connected" : "connect to read balances" }}</small>
                          </div>
                        </li>
                        <li class="bg-check">
                          <span class="bg-check-mark">2</span>
                          <div>
                            <b>Match the cluster</b>
                            <small>set your wallet to {{ SOLANA_NETWORK_NAME }}</small>
                          </div>
                        </li>
                        <li class="bg-check">
                          <span class="bg-check-mark">3</span>
                          <div>
                            <b>Keep a little SOL</b>
                            <small>{{ SOLANA_CLUSTER }} fees are paid in SOL</small>
                          </div>
                        </li>
                      </ul>
                    </div>
                    <div class="bg-sheet-foot">
                      <a
                        v-if="SOLANA_CLUSTER === 'devnet'"
                        class="bg-btn bg-btn--fill bg-btn--wide"
                        href="https://faucet.solana.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Get devnet SOL <Icon name="arrow-up-right" :size="14" />
                      </a>
                      <button
                        v-else
                        class="bg-btn bg-btn--fill bg-btn--wide"
                        type="button"
                        :disabled="connecting || busy"
                        @click="connected ? disconnectWallet() : connect()"
                      >
                        <Icon name="wallet" :size="15" />
                        {{ connected ? "Disconnect wallet" : "Connect wallet" }}
                      </button>
                    </div>
                  </section>

                  <div class="bg-note">
                    <Icon name="info" :size="18" />
                    <div>
                      <strong>Sample rows</strong>
                      <p>
                        Rows marked “sample” are examples. They never send a transaction and
                        disappear as soon as the program reads real data.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </section>
        </Transition>
    </main>

    <div
      v-if="txState.stage !== 'idle'"
      class="bg-toast"
      :data-tone="txState.stage === 'error' ? 'error' : txState.stage === 'success' ? 'success' : 'idle'"
      :role="txState.stage === 'error' ? 'alert' : 'status'"
      aria-live="polite"
      aria-atomic="true"
    >
      <span class="bg-toast-dot" aria-hidden="true"></span>
      <div class="bg-toast-copy">
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
        class="bg-command-icon bg-toast-close"
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
