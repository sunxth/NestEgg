<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <Logo :width="200" :height="100" />
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
            class="relative group bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-all duration-200 border-2 border-transparent hover:border-blue-500 focus:outline-none focus:border-blue-500"
          >
            <div class="flex flex-col items-center space-y-3">
              <!-- Husband Icon -->
              <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                <svg class="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C13.1 2 14 2.9 14 4S13.1 6 12 6 10 5.1 10 4 10.9 2 12 2M15.89 8.11C15.5 7.72 14.83 7 13.53 7C13.32 7 13.11 7.04 12.88 7.08C12.27 6.7 11.56 6.5 10.83 6.5C9.84 6.5 8.89 6.81 8.07 7.36C7.85 7.29 7.61 7.24 7.37 7.24C6.64 7.24 5.96 7.65 5.61 8.32C5.24 9 5.31 9.83 5.79 10.41L7 11.62V19C7 20.1 7.9 21 9 21H11V16H13V21H15C16.1 21 17 20.1 17 19V11.62L18.21 10.41C18.69 9.83 18.76 9 18.39 8.32C18.04 7.65 17.36 7.24 16.63 7.24C16.39 7.24 16.15 7.29 15.89 8.11Z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900">Husband</p>
                <p class="text-sm text-gray-500 mt-1">管理员账户</p>
              </div>
            </div>
          </button>

          <!-- Wife/User Card -->
          <button
            @click="selectRole('user')"
            class="relative group bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-all duration-200 border-2 border-transparent hover:border-pink-500 focus:outline-none focus:border-pink-500"
          >
            <div class="flex flex-col items-center space-y-3">
              <!-- Wife Icon -->
              <div class="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center group-hover:bg-pink-200 transition-colors">
                <svg class="w-12 h-12 text-pink-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C13.1 2 14 2.9 14 4S13.1 6 12 6 10 5.1 10 4 10.9 2 12 2M15.9 8.1C15.5 7.7 14.8 7 13.5 7H12.5C11.3 7 10.4 7.8 10.1 8.1C8.9 8.5 8 9.6 8 10.9V11.5L6.5 10C5.9 9.4 4.9 9.4 4.3 10S3.7 11.6 4.3 12.2L7 14.9V19C7 20.1 7.9 21 9 21H11V16H13V21H15C16.1 21 17 20.1 17 19V14.9L19.7 12.2C20.3 11.6 20.3 10.6 19.7 10S18.1 9.4 17.5 10L16 11.5V10.9C16 9.6 15.1 8.5 15.9 8.1Z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900">Wife</p>
                <p class="text-sm text-gray-500 mt-1">普通用户</p>
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
            class="text-sm text-indigo-600 hover:text-indigo-500"
          >
            ← 返回选择身份
          </button>
        </div>

        <div class="text-center mb-6">
          <div class="inline-flex items-center space-x-3">
            <div :class="[
              'w-16 h-16 rounded-full flex items-center justify-center',
              selectedRole === 'admin' ? 'bg-blue-100' : 'bg-pink-100'
            ]">
              <svg
                :class="[
                  'w-10 h-10',
                  selectedRole === 'admin' ? 'text-blue-600' : 'text-pink-600'
                ]"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path v-if="selectedRole === 'admin'" d="M12 2C13.1 2 14 2.9 14 4S13.1 6 12 6 10 5.1 10 4 10.9 2 12 2M15.89 8.11C15.5 7.72 14.83 7 13.53 7C13.32 7 13.11 7.04 12.88 7.08C12.27 6.7 11.56 6.5 10.83 6.5C9.84 6.5 8.89 6.81 8.07 7.36C7.85 7.29 7.61 7.24 7.37 7.24C6.64 7.24 5.96 7.65 5.61 8.32C5.24 9 5.31 9.83 5.79 10.41L7 11.62V19C7 20.1 7.9 21 9 21H11V16H13V21H15C16.1 21 17 20.1 17 19V11.62L18.21 10.41C18.69 9.83 18.76 9 18.39 8.32C18.04 7.65 17.36 7.24 16.63 7.24C16.39 7.24 16.15 7.29 15.89 8.11Z"/>
                <path v-else d="M12 2C13.1 2 14 2.9 14 4S13.1 6 12 6 10 5.1 10 4 10.9 2 12 2M15.9 8.1C15.5 7.7 14.8 7 13.5 7H12.5C11.3 7 10.4 7.8 10.1 8.1C8.9 8.5 8 9.6 8 10.9V11.5L6.5 10C5.9 9.4 4.9 9.4 4.3 10S3.7 11.6 4.3 12.2L7 14.9V19C7 20.1 7.9 21 9 21H11V16H13V21H15C16.1 21 17 20.1 17 19V14.9L19.7 12.2C20.3 11.6 20.3 10.6 19.7 10S18.1 9.4 17.5 10L16 11.5V10.9C16 9.6 15.1 8.5 15.9 8.1Z"/>
              </svg>
            </div>
            <div class="text-left">
              <p class="font-semibold text-gray-900">
                {{ selectedRole === 'admin' ? 'Husband' : 'Wife' }}
              </p>
              <p class="text-sm text-gray-500">
                {{ selectedRole === 'admin' ? '管理员账户' : '普通用户' }}
              </p>
            </div>
          </div>
        </div>

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
            :placeholder="selectedRole === 'admin' ? '请输入管理员密码' : '请输入用户密码'"
            autofocus
          />
        </div>

        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <p class="text-sm text-red-800">{{ error }}</p>
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