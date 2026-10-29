<script setup>
import brandMark from "../assets/rationum-mark.svg";

const emit = defineEmits(["navigate"]);
</script>

<template>
  <a
    class="bz-mast"
    :href="'#home'"
    aria-label="Rationum home"
    @click="emit('navigate', 'home')"
  >
    <img class="bz-mast-mark" :src="brandMark" width="42" height="42" alt="" />
    <span class="bz-mast-copy">
      <span class="bz-mast-word"><span class="bz-mast-signal">Ratio</span>num</span>
      <span class="bz-mast-tag">Time on the record</span>
    </span>
  </a>
</template>
