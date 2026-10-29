<script setup>
import brandMark from "../assets/actoria-mark.svg";

defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "home" },
});

const emit = defineEmits(["navigate"]);
</script>

<template>
  <div class="sp-brand">
    <a
      class="sp-brand-link"
      :href="'#home'"
      aria-label="Actoria home"
      @click="emit('navigate', 'home')"
    >
      <span class="sp-brand-mark" aria-hidden="true">
        <img :src="brandMark" width="34" height="34" alt="" />
      </span>
      <span class="sp-brand-text">
        <span class="sp-brand-word">Act<span class="sp-brand-accent">oria</span></span>
        <span class="sp-brand-tag">Time on the record</span>
      </span>
    </a>
  </div>
</template>
