<script setup>
import Icon from "../Icon.vue";

defineProps({
  options: { type: Array, default: () => [] },
  networkName: { type: String, default: "" },
});

const emit = defineEmits(["choose", "close"]);
</script>

<template>
  <div class="ax-veil" @click.self="emit('close')">
    <section class="ax-wallets" role="dialog" aria-modal="true" aria-labelledby="ax-wallet-title">
      <header class="ax-wallets-head">
        <div>
          <p class="ax-kicker"><span class="ax-kicker-dot" aria-hidden="true"></span>Connect</p>
          <h2 id="ax-wallet-title" class="ax-wallets-title">Choose a wallet</h2>
        </div>
        <button class="ax-command-icon" type="button" aria-label="Close wallet picker" @click="emit('close')">
          <Icon name="close" :size="18" />
        </button>
      </header>

      <p class="ax-wallets-note">
        Pick a wallet that can sign on {{ networkName || "this cluster" }}. Attesio only
        asks it to confirm quest rows, proposals and votes.
      </p>

      <ul v-if="options.length" class="ax-wallet-list">
        <li v-for="candidate in options" :key="candidate.name">
          <button class="ax-wallet-row" type="button" @click="emit('choose', candidate)">
            <img v-if="candidate.icon" :src="candidate.icon" alt="" width="28" height="28" />
            <span v-else class="ax-wallet-fallback" aria-hidden="true">
              <Icon name="wallet" :size="17" />
            </span>
            <span class="ax-wallet-name">{{ candidate.name }}</span>
            <Icon name="arrow-right" :size="15" />
          </button>
        </li>
      </ul>

      <p v-else class="ax-wallets-empty">
        No compatible wallet was detected in this browser. Install a Solana wallet
        extension, reload, then try again.
      </p>

      <footer class="ax-wallets-foot">
        <p>Nothing is signed until you approve it inside the wallet.</p>
        <button class="ax-btn ax-btn--line" type="button" @click="emit('close')">Cancel</button>
      </footer>
    </section>
  </div>
</template>
