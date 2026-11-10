<script setup>
import brandMark from "../assets/docketa-mark.svg";

const emit = defineEmits(["navigate"]);
</script>

<template>
  <a
    class="orb-seal"
    :href="'#home'"
    aria-label="Docketa home"
    @click="emit('navigate', 'home')"
  >
    <img class="orb-seal-mark" :src="brandMark" width="42" height="42" alt="" />
    <span class="orb-seal-copy">
      <span class="orb-seal-word"><span class="orb-seal-signal">Dock</span>eta</span>
      <span class="orb-seal-tag">Time on the record</span>
    </span>
  </a>
</template>
