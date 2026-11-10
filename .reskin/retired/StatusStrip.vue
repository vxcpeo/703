<script setup>
import brandMark from "../assets/docketa-mark.svg";

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
  <footer class="orb-colophon">
    <div class="orb-colophon-brand">
      <span class="orb-colophon-mark">
        <img :src="brandMark" width="26" height="26" alt="" />
      </span>
      <span class="orb-colophon-name"><span class="orb-colophon-signal">Dock</span>eta</span>
      <span class="orb-colophon-tag">Time on the record.</span>
    </div>
    <p class="orb-colophon-note">
      An independent project reading {{ networkName }}. Quests and advisory votes are
      recorded by a public Solana program; no token is minted, sold or promised here.
    </p>

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

    <div class="orb-colophon-word" aria-hidden="true"><span class="orb-colophon-word-signal">Dock</span>eta</div>

    <div class="orb-colophon-fine">
      <span>© 2026 Docketa · docketa.xyz. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
