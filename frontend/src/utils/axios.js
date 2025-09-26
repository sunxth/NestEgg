import axios from 'axios'

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 30000
})

// Request interceptor to add token to all requests
axiosInstance.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // If 401 Unauthorized, redirect to login
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')

      // Only redirect if not already on login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default axiosInstance