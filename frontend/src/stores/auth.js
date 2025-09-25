import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userRole = ref(localStorage.getItem('userRole') || '')

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userRole.value === 'admin')

  function setAuthHeader() {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  async function login(password, role = null) {
    try {
      const formData = new FormData()
      // Send role-specific username
      formData.append('username', role === 'admin' ? 'husband' : 'wife')
      formData.append('password', password)

      const response = await axios.post('/api/auth/login', formData)
      token.value = response.data.access_token

      const payload = JSON.parse(atob(token.value.split('.')[1]))
      userRole.value = payload.role

      localStorage.setItem('token', token.value)
      localStorage.setItem('userRole', userRole.value)
      setAuthHeader()

      return { success: true }
    } catch (error) {
      let errorMessage = '登录失败'
      if (error.response?.status === 401) {
        errorMessage = '密码错误，请重试'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      return {
        success: false,
        message: errorMessage
      }
    }
  }

  function logout() {
    token.value = ''
    userRole.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
    delete axios.defaults.headers.common['Authorization']
  }

  setAuthHeader()

  return {
    token,
    userRole,
    isAuthenticated,
    isAdmin,
    login,
    logout
  }
})