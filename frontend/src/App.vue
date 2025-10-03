<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
    <nav v-if="authStore.isAuthenticated" class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-12 h-12 rounded-full overflow-hidden bg-white shadow-sm">
                <Logo :width="48" :height="48" />
              </div>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="[
                  $route.path === item.href
                    ? 'border-b-2 border-indigo-500 text-gray-900 dark:text-white'
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-white'
                ]"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ authStore.isAdmin ? '管理员' : '普通用户' }}
            </span>
            <!-- Dark Mode Toggle -->
            <button
              @click="themeStore.toggleTheme()"
              class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              :title="themeStore.isDark ? '切换到亮色模式' : '切换到暗色模式'"
            >
              <!-- Sun Icon (Light Mode) -->
              <svg v-if="themeStore.isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
              </svg>
              <!-- Moon Icon (Dark Mode) -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
              </svg>
            </button>
            <button
              @click="logout"
              class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              退出
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Logo from '@/components/Logo.vue'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const navigation = [
  { name: '首页', href: '/' },
  { name: '交易', href: '/transactions' },
  { name: '日历', href: '/calendar' },
  { name: '统计', href: '/analytics' },
  { name: '设置', href: '/settings' }
]

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>