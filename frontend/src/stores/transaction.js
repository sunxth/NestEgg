import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '@/utils/axios'

export const useTransactionStore = defineStore('transaction', () => {
  const transactions = ref([])
  const monthlyStats = ref(null)
  const categoryStats = ref([])
  const loading = ref(false)

  async function fetchTransactions(params = {}) {
    loading.value = true
    try {
      const response = await axios.get('/api/transactions/', { params })
      transactions.value = response.data
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '获取记录失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchMonthlyStats(year, month = null) {
    try {
      const params = { year }
      if (month) params.month = month
      const response = await axios.get('/api/transactions/stats/monthly', { params })
      monthlyStats.value = response.data
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '获取统计失败'
      }
    }
  }

  async function fetchCategoryStats(params = {}) {
    try {
      const response = await axios.get('/api/transactions/stats/category', { params })
      categoryStats.value = response.data
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '获取分类统计失败'
      }
    }
  }

  async function createTransaction(data) {
    try {
      const response = await axios.post('/api/transactions/', data)
      await fetchTransactions()
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Create transaction error:', error.response?.data)
      // Handle validation errors
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // FastAPI validation error format
          const firstError = error.response.data.detail[0]
          return {
            success: false,
            message: firstError.msg || '数据格式错误'
          }
        }
        return {
          success: false,
          message: error.response.data.detail
        }
      }
      return {
        success: false,
        message: '创建记录失败'
      }
    }
  }

  async function updateTransaction(id, data) {
    try {
      const response = await axios.put(`/api/transactions/${id}`, data)
      await fetchTransactions()
      return { success: true, data: response.data }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '更新记录失败'
      }
    }
  }

  async function deleteTransaction(id) {
    try {
      await axios.delete(`/api/transactions/${id}`)
      await fetchTransactions()
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '删除记录失败'
      }
    }
  }

  async function exportCSV(params = {}) {
    try {
      const response = await axios.get('/api/export/csv', {
        params,
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `nestegg_export_${new Date().toISOString().split('T')[0]}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '导出失败'
      }
    }
  }

  return {
    transactions,
    monthlyStats,
    categoryStats,
    loading,
    fetchTransactions,
    fetchMonthlyStats,
    fetchCategoryStats,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    exportCSV
  }
})