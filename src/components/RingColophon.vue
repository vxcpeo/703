<script setup>
import brandMark from "../assets/docketa-mark.svg";
import Icon from "../Icon.vue";

defineProps({
  tabs: { type: Array, default: () => [] },
  networkName: { type: String, default: "" },
  cluster: { type: String, default: "" },
  programState: { type: String, default: "" },
  mintState: { type: String, default: "" },
  walletLabel: { type: String, default: "" },
  lastRead: { type: String, default: "" },
});

const emit = defineEmits(["navigate"]);

/* The single outbound link to the X account. It answers the website field on the
   profile, so both strands must carry the same string: @Docketa_top. */
const X_HANDLE = "@Docketa_top";
const X_URL = "https://x.com/Docketa_top";
const SITE_LABEL = "Docketa.top";
const SITE_URL = "https://www.docketa.top/";
</script>

<template>
  <footer class="orb-colophon">
    <span class="orb-colophon-rim" aria-hidden="true"></span>

    <div class="orb-colophon-brand">
      <span class="orb-colophon-mark">
        <img :src="brandMark" width="26" height="26" alt="" />
      </span>
      <span class="orb-colophon-name"><span class="orb-colophon-signal">Dock</span>eta</span>
      <span class="orb-colophon-tag">Time on the record.</span>
      <a
        class="orb-colophon-handle"
        :href="X_URL"
        target="_blank"
        rel="noopener noreferrer"
        :aria-label="`Docketa on X, ${X_HANDLE} — opens x.com in a new tab`"
      >
        <span class="orb-colophon-handle-net" aria-hidden="true">X</span>
        <span class="orb-colophon-handle-name">{{ X_HANDLE }}</span>
        <Icon name="external" :size="13" />
      </a>
    </div>

    <p class="orb-colophon-note">
      An independent project reading {{ networkName }}. Quests and advisory votes are
      recorded by a public Solana program; no token is minted, sold or promised here.
    </p>

    <div class="orb-colophon-grid">
      <div class="orb-colophon-block">
        <h3 class="orb-colophon-title">Explore</h3>
        <nav class="orb-colophon-links" aria-label="Footer">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            type="button"
            @click="emit('navigate', tab.id)"
          >{{ tab.label }}</button>
        </nav>
      </div>

      <div class="orb-colophon-block">
        <h3 class="orb-colophon-title">Network</h3>
        <div class="orb-colophon-facts">
          <div><span>Cluster</span><b>{{ cluster }}</b></div>
          <div><span>Network</span><b>{{ networkName }}</b></div>
          <div><span>Program</span><b>{{ programState }}</b></div>
          <div><span>Token mint</span><b>{{ mintState }}</b></div>
        </div>
      </div>

      <div class="orb-colophon-block">
        <h3 class="orb-colophon-title">Session</h3>
        <div class="orb-colophon-facts">
          <div><span>Wallet</span><b>{{ walletLabel }}</b></div>
          <div><span>Last read</span><b>{{ lastRead }}</b></div>
        </div>
        <p class="orb-colophon-note">
          Never share a seed phrase or private key to fix a connection.
        </p>
      </div>

      <div class="orb-colophon-block">
        <h3 class="orb-colophon-title">Elsewhere</h3>
        <div class="orb-colophon-facts">
          <div>
            <span>X</span>
            <b>
              <a :href="X_URL" target="_blank" rel="noopener noreferrer">{{ X_HANDLE }}</a>
            </b>
          </div>
          <div>
            <span>Site</span>
            <b><a :href="SITE_URL">{{ SITE_LABEL }}</a></b>
          </div>
        </div>
        <p class="orb-colophon-note">The register is open. Read it before you trust it.</p>
      </div>
    </div>

    <div class="orb-colophon-word" aria-hidden="true"><span class="orb-colophon-word-signal">Dock</span>eta</div>

    <div class="orb-colophon-fine">
      <span>© 2026 Docketa · {{ SITE_LABEL }}. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
