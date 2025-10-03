<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-48 h-48 rounded-full overflow-hidden bg-white shadow-lg">
            <Logo :width="192" :height="192" />
          </div>
        </div>
        <p class="mt-2 text-center text-sm text-gray-600">
          请选择您的身份
        </p>
      </div>

      <!-- Role Selection -->
      <div v-if="!selectedRole" class="mt-8 space-y-6">
        <div class="grid grid-cols-2 gap-4">
          <!-- Husband/Admin Card -->
          <button
            @click="selectRole('admin')"
            class="relative group bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md dark:shadow-gray-700/30 hover:shadow-xl dark:hover:shadow-gray-700/50 transition-all duration-200 border-2 border-transparent hover:border-blue-500 dark:hover:border-blue-400 focus:outline-none focus:border-blue-500 dark:focus:border-blue-400"
          >
            <div class="flex flex-col items-center space-y-3">
              <!-- Husband Icon -->
              <div class="w-20 h-20 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/40 dark:to-blue-800/40 rounded-full flex items-center justify-center group-hover:from-blue-200 group-hover:to-blue-300 dark:group-hover:from-blue-800/60 dark:group-hover:to-blue-700/60 transition-all shadow-inner">
                <svg class="w-12 h-12 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 dark:text-white">Husband</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">管理员账户</p>
              </div>
            </div>
          </button>

          <!-- Wife/User Card -->
          <button
            @click="selectRole('user')"
            class="relative group bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md dark:shadow-gray-700/30 hover:shadow-xl dark:hover:shadow-gray-700/50 transition-all duration-200 border-2 border-transparent hover:border-pink-500 dark:hover:border-pink-400 focus:outline-none focus:border-pink-500 dark:focus:border-pink-400"
          >
            <div class="flex flex-col items-center space-y-3">
              <!-- Wife Icon -->
              <div class="w-20 h-20 bg-gradient-to-br from-pink-100 to-pink-200 dark:from-pink-900/40 dark:to-pink-800/40 rounded-full flex items-center justify-center group-hover:from-pink-200 group-hover:to-pink-300 dark:group-hover:from-pink-800/60 dark:group-hover:to-pink-700/60 transition-all shadow-inner">
                <svg class="w-12 h-12 text-pink-600 dark:text-pink-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 dark:text-white">Wife</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">普通用户</p>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Password Form -->
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="text-center mb-4">
          <button
            type="button"
            @click="selectedRole = null; password = ''"
            class="text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300"
          >
            ← 返回选择身份
          </button>
        </div>

        <div class="text-center mb-6">
          <div class="inline-flex items-center space-x-3">
            <div :class="[
              'w-16 h-16 rounded-full flex items-center justify-center shadow-inner',
              selectedRole === 'admin' ? 'bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/40 dark:to-blue-800/40' : 'bg-gradient-to-br from-pink-100 to-pink-200 dark:from-pink-900/40 dark:to-pink-800/40'
            ]">
              <svg
                :class="[
                  'w-10 h-10',
                  selectedRole === 'admin' ? 'text-blue-600 dark:text-blue-400' : 'text-pink-600 dark:text-pink-400'
                ]"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
              </svg>
            </div>
            <div class="text-left">
              <p class="font-semibold text-gray-900 dark:text-white">
                {{ selectedRole === 'admin' ? 'Husband' : 'Wife' }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ selectedRole === 'admin' ? '管理员账户' : '普通用户' }}
              </p>
            </div>
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            密码
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            :placeholder="selectedRole === 'admin' ? '请输入管理员密码' : '请输入用户密码'"
            autofocus
          />
        </div>

        <div v-if="error" class="rounded-md bg-red-50 dark:bg-red-900/30 p-4">
          <p class="text-sm text-red-800 dark:text-red-200">{{ error }}</p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          :class="[
            'group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50',
            selectedRole === 'admin'
              ? 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
              : 'bg-pink-600 hover:bg-pink-700 focus:ring-pink-500'
          ]"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Logo from '@/components/Logo.vue'

const router = useRouter()
const authStore = useAuthStore()

const selectedRole = ref(null) // 'admin' or 'user'
const password = ref('')
const error = ref('')
const loading = ref(false)

function selectRole(role) {
  selectedRole.value = role
  error.value = ''
  password.value = ''
}

async function handleLogin() {
  error.value = ''
  loading.value = true

  const result = await authStore.login(password.value, selectedRole.value)

  if (result.success) {
    router.push('/')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>