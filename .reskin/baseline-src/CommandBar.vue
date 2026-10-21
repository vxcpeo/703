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
  <div class="bg-console">
    <div class="bg-console-top">
      <span v-if="cluster" class="bg-console-chip">
        <i class="bg-console-pulse" aria-hidden="true"></i>{{ cluster }}
      </span>
      <span class="bg-console-rule" aria-hidden="true"></span>
      <div class="bg-console-tools">
        <button
          class="bg-console-icon"
          type="button"
          :disabled="reading || busy"
          :aria-label="`Re-read ${cluster || 'network'} data`"
          @click="emit('sync')"
        >
          <Icon name="refresh" :size="18" :class="{ 'bg-spin': reading }" />
        </button>
        <button
          class="bg-btn bg-btn--fill bg-btn--sm"
          type="button"
          :disabled="connecting || busy"
          :aria-label="connected ? 'Disconnect wallet' : 'Connect a Solana wallet'"
          @click="emit('wallet')"
        >
          <Icon name="wallet" :size="16" />
          <span>{{ connecting ? "Connecting…" : walletLabel }}</span>
        </button>
        <button
          class="bg-console-icon"
          type="button"
          :aria-expanded="menuOpen ? 'true' : 'false'"
          aria-controls="ax-drawer"
          :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
          @click="emit('menu')"
        >
          <Icon :name="menuOpen ? 'close' : 'menu'" :size="20" />
        </button>
      </div>
    </div>
  </div>
</template>
