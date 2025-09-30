<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav v-if="authStore.isAuthenticated" class="bg-white shadow">
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
                    ? 'border-b-2 border-indigo-500 text-gray-900'
                    : 'text-gray-500 hover:text-gray-700'
                ]"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">
              {{ authStore.isAdmin ? '管理员' : '普通用户' }}
            </span>
            <button
              @click="logout"
              class="text-sm text-gray-500 hover:text-gray-700"
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
import Logo from '@/components/Logo.vue'

const router = useRouter()
const authStore = useAuthStore()

const navigation = [
  { name: '首页', href: '/' },
  { name: '记账', href: '/transactions' },
  { name: '收支', href: '/cashflow' },
  { name: '日历', href: '/calendar' },
  { name: '统计', href: '/analytics' },
  { name: '设置', href: '/settings' }
]

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>