<script setup>
import Icon from "../Icon.vue";

defineProps({
  options: { type: Array, default: () => [] },
  networkName: { type: String, default: "" },
});

const emit = defineEmits(["choose", "close"]);
</script>

<template>
  <div class="orb-picker-veil" @click.self="emit('close')">
    <section class="orb-picker" role="dialog" aria-modal="true" aria-labelledby="orb-picker-title">
      <span class="orb-picker-orbit" aria-hidden="true"></span>
      <header class="orb-picker-head">
        <div>
          <p class="orb-kicker"><span class="orb-kicker-dot" aria-hidden="true"></span>Connect</p>
          <h2 id="orb-picker-title" class="orb-picker-title">Choose a wallet</h2>
        </div>
        <button class="orb-iconbtn" type="button" aria-label="Close wallet picker" @click="emit('close')">
          <Icon name="close" :size="18" />
        </button>
      </header>

      <p class="orb-picker-note">
        Pick a wallet that can sign on {{ networkName || "this cluster" }}. Docketa only
        asks it to confirm quest rows, proposals and votes.
      </p>

      <ul v-if="options.length" class="orb-picker-list">
        <li v-for="candidate in options" :key="candidate.name">
          <button class="orb-picker-row" type="button" @click="emit('choose', candidate)">
            <img v-if="candidate.icon" :src="candidate.icon" alt="" width="28" height="28" />
            <span v-else class="orb-picker-fallback" aria-hidden="true">
              <Icon name="wallet" :size="17" />
            </span>
            <span class="orb-picker-name">{{ candidate.name }}</span>
            <Icon name="arrow-right" :size="15" />
          </button>
        </li>
      </ul>

      <p v-else class="orb-picker-empty">
        No compatible wallet was detected in this browser. Install a Solana wallet
        extension, reload, then try again.
      </p>

      <footer class="orb-picker-foot">
        <p>Nothing is signed until you approve it inside the wallet.</p>
        <button class="orb-btn orb-btn--wire" type="button" @click="emit('close')">Cancel</button>
      </footer>
    </section>
  </div>
</template>
