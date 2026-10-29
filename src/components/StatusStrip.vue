<script setup>
import brandMark from "../assets/rationum-mark.svg";

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
  <footer class="bz-colophon">
    <div class="bz-colophon-brand">
      <span class="bz-colophon-mark">
        <img :src="brandMark" width="26" height="26" alt="" />
      </span>
      <span class="bz-colophon-name"><span class="bz-colophon-signal">Ratio</span>num</span>
      <span class="bz-colophon-tag">Time on the record.</span>
    </div>
    <p class="bz-colophon-note">
      An independent project reading {{ networkName }}. Quests and advisory votes are
      recorded by a public Solana program; no token is minted, sold or promised here.
    </p>

    <div class="bz-colophon-block">
      <h3 class="bz-colophon-title">Explore</h3>
      <nav class="bz-colophon-links" aria-label="Footer">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          @click="emit('navigate', tab.id)"
        >{{ tab.label }}</button>
      </nav>
    </div>

    <div class="bz-colophon-block">
      <h3 class="bz-colophon-title">Network</h3>
      <div class="bz-colophon-facts">
        <div><span>Cluster</span><b>{{ cluster }}</b></div>
        <div><span>Network</span><b>{{ networkName }}</b></div>
        <div><span>Program</span><b>{{ programState }}</b></div>
        <div><span>Token mint</span><b>{{ mintState }}</b></div>
      </div>
    </div>

    <div class="bz-colophon-block">
      <h3 class="bz-colophon-title">Session</h3>
      <div class="bz-colophon-facts">
        <div><span>Wallet</span><b>{{ walletLabel }}</b></div>
        <div><span>Last read</span><b>{{ lastRead }}</b></div>
      </div>
      <p class="bz-colophon-note">
        Never share a seed phrase or private key to fix a connection.
      </p>
    </div>

    <div class="bz-colophon-word" aria-hidden="true"><span class="bz-colophon-word-signal">Ratio</span>num</div>

    <div class="bz-colophon-fine">
      <span>© 2026 Rationum · rationum.xyz. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
