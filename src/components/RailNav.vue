<script setup>
import Icon from "../Icon.vue";
import brandMark from "../assets/clepsyra-mark.svg";

defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "home" },
});

const emit = defineEmits(["navigate"]);
</script>

<template>
  <nav class="bg-index" aria-label="Primary">
    <a
      class="bg-brandline"
      :href="'#home'"
      aria-label="Clepsyra home"
      @click="emit('navigate', 'home')"
    >
      <span class="bg-brandline-mark" aria-hidden="true">
        <img :src="brandMark" width="26" height="26" alt="" />
      </span>
      <span class="bg-brandline-text">
        <span class="bg-brandline-word">Cleps<span class="bg-brandline-accent">yra</span></span>
        <span class="bg-brandline-tag">Time on the record</span>
      </span>
    </a>

    <ol class="bg-index-list">
      <li v-for="tab in tabs" :key="tab.id">
        <a
          class="bg-index-link"
          :href="'#' + tab.id"
          :aria-current="active === tab.id ? 'page' : undefined"
          @click="emit('navigate', tab.id)"
        >
          <span class="bg-index-glyph" aria-hidden="true"><Icon :name="tab.icon" :size="17" /></span>
          <span class="bg-index-label">{{ tab.label }}</span>
          <b v-if="tab.badge !== null && tab.badge !== undefined" class="bg-index-badge">{{ tab.badge }}</b>
        </a>
      </li>
    </ol>

    <span class="bg-index-rule" aria-hidden="true"></span>
  </nav>
</template>
