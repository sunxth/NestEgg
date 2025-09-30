<template>
  <div class="logo-container">
    <img
      :src="logoUrl"
      :alt="alt"
      :width="width"
      :height="height"
      class="logo"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import logoImage from '@/assets/logo.png'

const props = defineProps({
  width: {
    type: [String, Number],
    default: 120
  },
  height: {
    type: [String, Number],
    default: 120
  },
  alt: {
    type: String,
    default: 'NestEgg Logo'
  }
})

const logoUrl = computed(() => logoImage)
</script>

<style scoped>
.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.logo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transform: scale(1.5);
}
</style>