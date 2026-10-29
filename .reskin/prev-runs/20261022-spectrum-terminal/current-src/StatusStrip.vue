<script setup>
import brandMark from "../assets/actoria-mark.svg";

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
  <footer class="sp-status">
    <div class="sp-status-top">
      <div class="sp-status-brand">
        <span class="sp-status-mark">
          <img :src="brandMark" width="26" height="26" alt="" />
        </span>
        <span class="sp-status-name">Act<span class="sp-status-accent">oria</span></span>
        <span class="sp-status-tag">Time on the record.</span>
      </div>
      <p class="sp-status-note">
        An independent project reading {{ networkName }}. Quests and advisory votes are
        recorded by a public Solana program; no token is minted, sold or promised here.
      </p>
    </div>

    <div class="sp-status-cols">
      <div class="sp-status-col">
        <h3>Explore</h3>
        <nav class="sp-status-links" aria-label="Footer">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            type="button"
            @click="emit('navigate', tab.id)"
          >{{ tab.label }}</button>
        </nav>
      </div>

      <div class="sp-status-col">
        <h3>Network</h3>
        <div class="sp-status-facts">
          <div><span>Cluster</span><b>{{ cluster }}</b></div>
          <div><span>Network</span><b>{{ networkName }}</b></div>
          <div><span>Program</span><b>{{ programState }}</b></div>
          <div><span>Token mint</span><b>{{ mintState }}</b></div>
        </div>
      </div>

      <div class="sp-status-col">
        <h3>Session</h3>
        <div class="sp-status-facts">
          <div><span>Wallet</span><b>{{ walletLabel }}</b></div>
          <div><span>Last read</span><b>{{ lastRead }}</b></div>
        </div>
        <p class="sp-status-note">
          Never share a seed phrase or private key to fix a connection.
        </p>
      </div>
    </div>

    <div class="sp-status-word" aria-hidden="true">Act<span class="sp-status-word-accent">oria</span></div>

    <div class="sp-status-fine">
      <span>© 2026 Actoria · actoria.xyz. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
