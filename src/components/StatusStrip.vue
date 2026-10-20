<script setup>
import brandMark from "../assets/attesio-mark.svg";

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
</script>

<template>
  <footer class="ax-status">
    <div class="ax-status-top">
      <div class="ax-status-brand">
        <span class="ax-status-mark">
          <img :src="brandMark" width="26" height="26" alt="" />
          <b>Attes<span class="ax-status-io">io</span></b>
        </span>
        <p class="ax-status-tag">Time on the record.</p>
        <p class="ax-status-note">
          An independent project reading {{ networkName }}. Quests and advisory votes are
          recorded by a public Solana program; no token is minted, sold or promised here.
        </p>
      </div>

      <div class="ax-status-cols">
        <div class="ax-status-col">
          <h3>Explore</h3>
          <nav class="ax-status-links" aria-label="Footer">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              @click="emit('navigate', tab.id)"
            >{{ tab.label }}</button>
          </nav>
        </div>

        <div class="ax-status-col">
          <h3>Network</h3>
          <div class="ax-status-facts">
            <div><span>Cluster</span><b>{{ cluster }}</b></div>
            <div><span>Network</span><b>{{ networkName }}</b></div>
            <div><span>Program</span><b>{{ programState }}</b></div>
            <div><span>Token mint</span><b>{{ mintState }}</b></div>
          </div>
        </div>

        <div class="ax-status-col">
          <h3>Session</h3>
          <div class="ax-status-facts">
            <div><span>Wallet</span><b>{{ walletLabel }}</b></div>
            <div><span>Last read</span><b>{{ lastRead }}</b></div>
          </div>
          <p class="ax-status-note">
            Never share a seed phrase or private key to fix a connection.
          </p>
        </div>
      </div>
    </div>

    <div class="ax-status-word" aria-hidden="true">Attes<span class="ax-status-word-io">io</span></div>

    <div class="ax-status-fine">
      <span>© 2026 Attesio · attesio.xyz. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
