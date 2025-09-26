<template>
  <svg
    :width="width"
    :height="height"
    viewBox="0 0 200 100"
    xmlns="http://www.w3.org/2000/svg"
    class="logo"
  >
    <defs>
      <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
      </linearGradient>
    </defs>

    <!-- 鸟巢 -->
    <ellipse cx="60" cy="65" rx="35" ry="20" fill="#8B4513" stroke="#A0522D" stroke-width="2"/>
    <ellipse cx="60" cy="55" rx="28" ry="15" fill="#CD853F" stroke="#A0522D" stroke-width="2"/>

    <!-- 蛋 -->
    <circle cx="75" cy="50" r="12" fill="#FFFFFF" stroke="#CCCCCC" stroke-width="1"/>
    <circle cx="50" cy="55" r="12" fill="#FFFFFF" stroke="#CCCCCC" stroke-width="1"/>

    <!-- 文字 -->
    <text
      x="105"
      y="60"
      font-family="Arial, sans-serif"
      font-size="30"
      font-weight="bold"
      fill="url(#grad1)"
    >
      NestEgg
    </text>

    <text
      x="105"
      y="80"
      font-family="Arial, sans-serif"
      font-size="14"
      fill="#666666"
    >
      Smart Family Budgeting
    </text>
  </svg>
</template>

<script setup>
defineProps({
  width: {
    type: [String, Number],
    default: 120
  },
  height: {
    type: [String, Number],
    default: 60
  }
})
</script>

<style scoped>
.logo {
  display: block;
}
</style>