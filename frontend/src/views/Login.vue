<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          NestEgg 家庭记账
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          请输入密码登录
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            密码
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="输入管理员密码或用户密码"
          />
        </div>

        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <p class="text-sm text-red-800">{{ error }}</p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
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

const router = useRouter()
const authStore = useAuthStore()

const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true

  const result = await authStore.login(password.value)

  if (result.success) {
    router.push('/')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>