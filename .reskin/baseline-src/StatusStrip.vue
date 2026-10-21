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
  <footer class="bg-colophon">
    <div class="bg-colophon-brand">
      <span class="bg-colophon-mark">
        <img :src="brandMark" width="24" height="24" alt="" />
      </span>
      <span class="bg-colophon-name">Act<span class="bg-colophon-accent">oria</span></span>
      <span class="bg-colophon-tag">Time on the record.</span>
    </div>

    <p class="bg-colophon-note">
      An independent project reading {{ networkName }}. Quests and advisory votes are
      recorded by a public Solana program; no token is minted, sold or promised here.
    </p>

    <div class="bg-colophon-cols">
      <div class="bg-colophon-col">
        <h3>Explore</h3>
        <nav class="bg-colophon-links" aria-label="Footer">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            type="button"
            @click="emit('navigate', tab.id)"
          >{{ tab.label }}</button>
        </nav>
      </div>

      <div class="bg-colophon-col">
        <h3>Network</h3>
        <div class="bg-colophon-facts">
          <div><span>Cluster</span><b>{{ cluster }}</b></div>
          <div><span>Network</span><b>{{ networkName }}</b></div>
          <div><span>Program</span><b>{{ programState }}</b></div>
          <div><span>Token mint</span><b>{{ mintState }}</b></div>
        </div>
      </div>

      <div class="bg-colophon-col">
        <h3>Session</h3>
        <div class="bg-colophon-facts">
          <div><span>Wallet</span><b>{{ walletLabel }}</b></div>
          <div><span>Last read</span><b>{{ lastRead }}</b></div>
        </div>
        <p class="bg-colophon-note">
          Never share a seed phrase or private key to fix a connection.
        </p>
      </div>
    </div>

    <div class="bg-colophon-word" aria-hidden="true">Act<span class="bg-colophon-word-accent">oria</span></div>

    <div class="bg-colophon-fine">
      <span>© 2026 Actoria · actoria.xyz. Written to be reopened.</span>
      <span>Independent community project · not affiliated with the Solana Foundation.</span>
    </div>
  </footer>
</template>
