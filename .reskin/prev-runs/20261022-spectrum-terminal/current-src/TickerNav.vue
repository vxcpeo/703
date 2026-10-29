<script setup>
import Icon from "../Icon.vue";

defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "home" },
});

const emit = defineEmits(["navigate"]);
</script>

<template>
  <nav class="sp-ticker" aria-label="Primary">
    <ol class="sp-ticker-list">
      <li v-for="tab in tabs" :key="tab.id" class="sp-ticker-item">
        <a
          class="sp-ticker-link"
          :href="'#' + tab.id"
          :aria-current="active === tab.id ? 'page' : undefined"
          @click="emit('navigate', tab.id)"
        >
          <span class="sp-ticker-glyph" aria-hidden="true"><Icon :name="tab.icon" :size="15" /></span>
          <span class="sp-ticker-label">{{ tab.label }}</span>
          <b v-if="tab.badge !== null && tab.badge !== undefined" class="sp-ticker-badge">{{ tab.badge }}</b>
        </a>
      </li>
    </ol>
  </nav>
</template>
