<script setup>
defineProps({
  name: { type: String, default: "arrow-right" },
  size: { type: [Number, String], default: 20 },
});

/* Single-stroke geometric set: 24 unit box, no fills, consistent 1.6 weight. */
const paths = {
  portico: "M3 21h18 M5 21V9l7-4.6L19 9v12 M9.5 21v-5.4h5V21 M7.5 12.5h9",
  flag: "M6 21V3.8 M6 4.4h11.4l-1.9 3.4 1.9 3.4H6",
  ballot:
    "M5 10.6h14V20H5z M8.6 10.6V5.2A1.7 1.7 0 0 1 10.3 3.5h3.4a1.7 1.7 0 0 1 1.7 1.7v5.4 M9.6 15.4l1.9 1.9 3.6-3.6",
  safe:
    "M4 3.8h16v16.4H4z M12 8.6a3.4 3.4 0 1 0 0 6.8 3.4 3.4 0 0 0 0-6.8 M15.4 15.4l2.6 2.6 M4 7.4h1.6 M18.4 7.4H20",
  coin:
    "M12 20.5a8.5 8.5 0 1 0 0-17 8.5 8.5 0 0 0 0 17 M12 15.6a3.6 3.6 0 1 0 0-7.2 3.6 3.6 0 0 0 0 7.2",
  book:
    "M12 6.6C10 4.9 6.9 4.6 4.1 5.5v13.1c2.8-.9 5.9-.6 7.9 1.1 2-1.7 5.1-2 7.9-1.1V5.5c-2.8-.9-5.9-.6-7.9 1.1z M12 6.6v13.1",
  menu: "M3.5 7h17 M3.5 12h17 M3.5 17h17",
  close: "M6.4 6.4l11.2 11.2 M17.6 6.4L6.4 17.6",
  refresh:
    "M4 12a8 8 0 0 1 13.7-5.6L20 8.6 M20 4.2v4.4h-4.4 M20 12a8 8 0 0 1-13.7 5.6L4 15.4 M4 19.8v-4.4h4.4",
  wallet:
    "M4 7.4h12.5A2.5 2.5 0 0 1 19 9.9v6.7a2.4 2.4 0 0 1-2.4 2.4H5.4A2.4 2.4 0 0 1 3 16.6V6.4A2.4 2.4 0 0 1 5.4 4h9.1 M15.8 13.6h1.6",
  search: "M17.2 17.2 21 21 M18.4 10.9a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0",
  "arrow-right": "M4 12h14.5 M12.8 5.8 19 12l-6.2 6.2",
  "arrow-up-right": "M6.8 17.2 17.2 6.8 M8.4 6.8h8.8v8.8",
  "chevron-down": "M6.6 9.4 12 14.8l5.4-5.4",
  check: "M4.8 12.6 9.2 17 19.2 7",
  info: "M12 10.8v5.4 M12 7.4v.3 M20.5 12a8.5 8.5 0 1 1-17 0 8.5 8.5 0 0 1 17 0",
  alert: "M12 4.2 21 20H3z M12 9.8v4.4 M12 17.2v.3",
  shield:
    "M12 3.4l7.4 3.1v5.7c0 4.3-4.7 7.5-7.4 8.5-2.7-1-7.4-4.2-7.4-8.5V6.5z M8.9 12l2.2 2.2 4.1-4.3",
  plus: "M12 5v14 M5 12h14",
  minus: "M5 12h14",
  clock: "M12 7.4V12l3.1 1.9 M20.5 12a8.5 8.5 0 1 1-17 0 8.5 8.5 0 0 1 17 0",
  external:
    "M13.6 4.5h5.9v5.9 M19.5 4.5 11 13 M17 15.2v3.4A1.9 1.9 0 0 1 15.1 20.5H5.4A1.9 1.9 0 0 1 3.5 18.6V8.9A1.9 1.9 0 0 1 5.4 7h3.4",
  spark: "M12 3.4l2.2 6.4 6.4 2.2-6.4 2.2L12 20.6l-2.2-6.4L3.4 12l6.4-2.2z",
  users:
    "M9.2 11.4a3.3 3.3 0 1 0 0-6.6 3.3 3.3 0 0 0 0 6.6z M3.6 19.8c0-3.1 2.5-5.2 5.6-5.2s5.6 2.1 5.6 5.2 M16.1 5.2a3.3 3.3 0 0 1 0 6.4 M17.6 14.9c1.9.5 3.2 2.3 3.2 4.6",
};
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.6"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    focusable="false"
  >
    <path :d="paths[name] || paths['arrow-right']" />
  </svg>
</template>
