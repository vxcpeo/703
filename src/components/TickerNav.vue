<script setup>
import Icon from "../Icon.vue";

defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "home" },
});

const emit = defineEmits(["navigate"]);
</script>

<template>
  <nav class="bz-index" aria-label="Primary">
    <ol class="bz-index-list">
      <li v-for="(tab, position) in tabs" :key="tab.id" class="bz-index-item">
        <a
          class="bz-index-link"
          :href="'#' + tab.id"
          :aria-current="active === tab.id ? 'page' : undefined"
          @click="emit('navigate', tab.id)"
        >
          <span class="bz-index-num" aria-hidden="true">{{ String(position + 1).padStart(2, "0") }}</span>
          <span class="bz-index-glyph" aria-hidden="true"><Icon :name="tab.icon" :size="17" /></span>
          <span class="bz-index-label">{{ tab.label }}</span>
          <b v-if="tab.badge !== null && tab.badge !== undefined" class="bz-index-badge">{{ tab.badge }}</b>
        </a>
      </li>
    </ol>
  </nav>
</template>
