<script setup>
import Icon from "../Icon.vue";

defineProps({
  options: { type: Array, default: () => [] },
  networkName: { type: String, default: "" },
});

const emit = defineEmits(["choose", "close"]);
</script>

<template>
  <div class="sp-veil" @click.self="emit('close')">
    <section class="sp-wallet" role="dialog" aria-modal="true" aria-labelledby="sp-wallet-title">
      <header class="sp-wallet-head">
        <div>
          <p class="sp-eyebrow"><span class="sp-eyebrow-dot" aria-hidden="true"></span>Connect</p>
          <h2 id="sp-wallet-title" class="sp-wallet-title">Choose a wallet</h2>
        </div>
        <button class="sp-icon-btn" type="button" aria-label="Close wallet picker" @click="emit('close')">
          <Icon name="close" :size="18" />
        </button>
      </header>

      <p class="sp-wallet-note">
        Pick a wallet that can sign on {{ networkName || "this cluster" }}. Actoria only
        asks it to confirm quest rows, proposals and votes.
      </p>

      <ul v-if="options.length" class="sp-wallet-list">
        <li v-for="candidate in options" :key="candidate.name">
          <button class="sp-wallet-row" type="button" @click="emit('choose', candidate)">
            <img v-if="candidate.icon" :src="candidate.icon" alt="" width="28" height="28" />
            <span v-else class="sp-wallet-fallback" aria-hidden="true">
              <Icon name="wallet" :size="17" />
            </span>
            <span class="sp-wallet-name">{{ candidate.name }}</span>
            <Icon name="arrow-right" :size="15" />
          </button>
        </li>
      </ul>

      <p v-else class="sp-wallet-empty">
        No compatible wallet was detected in this browser. Install a Solana wallet
        extension, reload, then try again.
      </p>

      <footer class="sp-wallet-foot">
        <p>Nothing is signed until you approve it inside the wallet.</p>
        <button class="sp-btn sp-btn--line" type="button" @click="emit('close')">Cancel</button>
      </footer>
    </section>
  </div>
</template>
