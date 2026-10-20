<script setup>
import Icon from "../Icon.vue";
import brandMark from "../assets/attesio-mark.svg";

defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "home" },
});

const emit = defineEmits(["navigate"]);
</script>

<template>
  <nav class="ax-rail" aria-label="Primary">
    <a
      class="ax-spine-brand"
      :href="'#home'"
      aria-label="Attesio home"
      @click="emit('navigate', 'home')"
    >
      <span class="ax-spine-mark" aria-hidden="true">
        <img :src="brandMark" width="26" height="26" alt="" />
      </span>
      <span class="ax-spine-text">
        <span class="ax-spine-word">Attes<span class="ax-spine-io">io</span></span>
        <span class="ax-spine-tag">Time on the record</span>
      </span>
    </a>

    <div class="ax-rail-list">
      <a
        v-for="tab in tabs"
        :key="tab.id"
        class="ax-rail-item"
        :href="'#' + tab.id"
        :aria-current="active === tab.id ? 'page' : undefined"
        @click="emit('navigate', tab.id)"
      >
        <span class="ax-rail-glyph" aria-hidden="true"><Icon :name="tab.icon" :size="17" /></span>
        <span class="ax-rail-label">{{ tab.label }}</span>
        <b v-if="tab.badge !== null && tab.badge !== undefined" class="ax-rail-badge">{{ tab.badge }}</b>
      </a>
    </div>

    <span class="ax-rail-foot" aria-hidden="true"><i></i></span>
  </nav>
</template>
