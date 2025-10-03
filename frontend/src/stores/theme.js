import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 从 localStorage 读取或使用默认值
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  // 切换主题
  function toggleTheme() {
    isDark.value = !isDark.value
  }

  // 设置主题
  function setTheme(dark) {
    isDark.value = dark
  }

  // 监听主题变化，更新 localStorage 和 HTML class
  watch(isDark, (newValue) => {
    localStorage.setItem('theme', newValue ? 'dark' : 'light')

    if (newValue) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, { immediate: true })

  return {
    isDark,
    toggleTheme,
    setTheme
  }
})
