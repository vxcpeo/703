<script setup>
import Icon from "../Icon.vue";

defineProps({
  walletLabel: { type: String, default: "Connect wallet" },
  connected: { type: Boolean, default: false },
  reading: { type: Boolean, default: false },
  busy: { type: Boolean, default: false },
  connecting: { type: Boolean, default: false },
  cluster: { type: String, default: "" },
  menuOpen: { type: Boolean, default: false },
});

const emit = defineEmits(["sync", "wallet", "menu"]);
</script>

<template>
  <div class="bz-dock">
    <span v-if="cluster" class="bz-dock-chip">
      <i class="bz-dock-pulse" aria-hidden="true"></i>{{ cluster }}
    </span>
    <div class="bz-dock-tools">
      <button
        class="bz-icon-btn"
        type="button"
        :disabled="reading || busy"
        :aria-label="`Re-read ${cluster || 'network'} data`"
        @click="emit('sync')"
      >
        <Icon name="refresh" :size="18" :class="{ 'bz-spin': reading }" />
      </button>
      <button
        class="bz-icon-btn"
        type="button"
        :aria-expanded="menuOpen ? 'true' : 'false'"
        aria-controls="ax-drawer"
        :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
        @click="emit('menu')"
      >
        <Icon :name="menuOpen ? 'close' : 'menu'" :size="20" />
      </button>
    </div>
    <button
      class="bz-btn bz-btn--fill bz-btn--sm bz-dock-wallet"
      type="button"
      :disabled="connecting || busy"
      :aria-label="connected ? 'Disconnect wallet' : 'Connect a Solana wallet'"
      @click="emit('wallet')"
    >
      <Icon name="wallet" :size="16" />
      <span>{{ connecting ? "Connecting…" : walletLabel }}</span>
    </button>
  </div>
</template>
